# Copyright (C) 2012 Ben Webb <bjwebb67@googlemail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import xlrd
from lxml.builder import ElementMaker
import lxml.etree as etree
import datetime
import parsedatetime.parsedatetime as pdt

# structure.py contains the mappings between the spreadsheet and the XML files 
# and also all the information required to generate the schema
import structure

datemode = None
def get_date(value):
    """ Helper function to return the xml date string for a given
        spreadsheet cell value.
    
    """
    global datemode
    try:
        date = datetime.datetime(*xlrd.xldate_as_tuple(value, datemode))
        return date.date().isoformat()
    except ValueError:
        return ''

def datetimestamp():
    """ Helper function to produce a nice ISO string for the current date
        and time.

    """
    class GuessTimezone(datetime.tzinfo):
        def utcoffset(self, dt):
            td = datetime.datetime.now() - datetime.datetime.utcnow()
            return datetime.timedelta(hours=round(td.seconds/3600.0),
                                      minutes=(round(td.seconds/60.0))%60)
        def dst(self, dt):
            return datetime.timedelta(seconds=0) 
    now = datetime.datetime.now(GuessTimezone())
    now -= datetime.timedelta(microseconds=now.microsecond)
    return now.isoformat()

def use_code(heading, text, codes=structure.codes):
    """ Helper function to return the short code for a given heading
        and text value.

    """
    if heading in codes:
        if text == '': return ''
        return codes[heading][text]
    else:
        return text


def parse_data(root, sheet, rows):
    """ Parse a 'data' sheet.
        ie. Activity Data or Organisation Data

        root -- an xml element to append to
        sheet -- the xlrd sheet element to parse
        rows -- a list of xml tags that correspond to each row
        
    """
    for rowx,rowname in enumerate(rows):
        if rowname == '':
            continue
        if isinstance(rowname, tuple):
            rowxml = etree.SubElement(root, rowname[0])
            rowxml.attrib['type'] = rowname[2]
        else:
            rowxml = etree.SubElement(root, rowname)
        
        for colx, heading in enumerate(structure.header):
            if heading == '':
                continue
            try:
                cell = sheet.cell_value(rowx=rowx, colx=colx)
            except IndexError:
                continue
            if heading in structure.codes_activity:
                el = etree.SubElement(rowxml, heading)
                if heading == 'exclusions':
                    narrative_el = etree.SubElement(el, 'narrative')
                    narrative_el.text = unicode(cell)
                    try:
                        attrib_cell = unicode(sheet.cell_value(rowx=rowx, colx=colx+1))
                    except IndexError:
                        continue
                else:
                    attrib_cell = cell
                if attrib_cell == '':
                    continue
                else:
                    el.attrib['category'] = use_code(heading,
                                        unicode(attrib_cell),
                                        codes=structure.codes_activity)
            else:
                if heading in structure.date_tags:
                    cell = get_date(cell)
                else:
                    cell = unicode(cell)
                if cell != '':
                    el = etree.SubElement(rowxml, heading)
                    el.text = cell
    return root


def parse_information(root, sheet, rows):
    """ Parse the Publisher Information sheet

        root -- an xml element to append to
        sheet -- the xlrd sheet element to parse
        rows -- a list of tuples containing structural
                information about each cell in the sheet 

    """
    for rowx,row in enumerate(rows):
        if row:
            el = etree.SubElement(root, row[1])
            narrative_el = etree.SubElement(el, 'narrative')
            row_data = sheet.row(rowx)
            if row[4] == 'narrative':
                for i in 2,3:
                    if row[i] != '':
                        if row[i] in structure.date_tags:
                            d = get_date(row_data[i].value)
                            if d != '':
                                el.attrib[row[i]] = d
                        else:
                            el.attrib[row[i]] = use_code(row[i],
                                    unicode(row_data[i].value))
                narrative_el.text = row_data[4].value
            else:
                narrative_el.text = "".join(map(lambda x: x.value, row_data[2:4]))
                
    return root
    

def silent_value(sheet, **args):
    """ Helper function to fetch cell values and convert them to strings,
        whilst ignoring possible exceptions (ie. if a cell does not exist).

        Also make sure all values are returned as unicode, and that integers
        are formatted correctly. 

    """
    try:
        value = sheet.cell_value(**args)
        if isinstance(value, float):
            if value == round(value):
                return unicode(int(value))
            else:
                return unicode(value)
        else:
            return value
    except IndexError:
        return ''


def full_xml(spreadsheet):
    """ Print the full parsed xml for the given spreadsheet filename"""
    global datemode
    global E
    E = ElementMaker()
    book = xlrd.open_workbook(spreadsheet)
    datemode = book.datemode
    sheet = book.sheet_by_index(0)

    # TODO Add handling of proper excel dates
    pdt_cal = pdt.Calendar()
    date_tuple = pdt_cal.parse(silent_value(sheet, rowx=6, colx=6))
    datestring = '-'.join([str(x).zfill(2) for x in date_tuple[0][0:3]])

    # TODO Make default language configurable
    root = lang("en", E.implementation(
        E.metadata(
            E.publisher(
                silent_value(sheet, rowx=2, colx=6),
                code=silent_value(sheet, rowx=4, colx=6)
            ),
            E.version(silent_value(sheet, rowx=6, colx=3)),
            E.date(datestring) 
        ),
        parse_information(
            E.publishing(),
            book.sheet_by_index(1),
            structure.publishing_rows
        ),
        parse_data(
            E.organisation(),
            book.sheet_by_index(2),
            structure.organisation_rows
        ),
        parse_data(
            E.activity(),
            book.sheet_by_index(3),
            structure.activity_rows
        )
    ))
    root.set('generated-datetime', datetimestamp())
    return root


def sheetschema(root, sheetname):
    """ Produce the schema elements for the named sheet.

        root -- an xml element to append to
        sheetname -- the short name of a sheet, as used in the structure
                     data and as the xml tag name.
                     Possible values are 'activity' and 'organisation'

    """
    global E
    rows = vars(structure)[sheetname+'_rows'] 
    docs = vars(structure)[sheetname+'_docs']
    #tuple_rows_done = {}
    ann = {
        "activity": """
        Contains information about the data provider's plans to implement
        specific parts of the activity data.

        Each of the child elements if either an informationArea, or a
        list of informationAreas.

        """, "organisation":"""
        Contains information about the data provider's plans to implement
        specific parts of the organisation data.

        """
    }
    choice_el = E.choice(maxOccurs="unbounded")
    root.append(
        E.element(
            E.annotation(lang("en", E.documentation(ann[sheetname]))),
            E.complexType(
                choice_el
            ),
            name=sheetname
        )
    )
    tuple_rows_done = {}
    for rowx,rowname in enumerate(rows):
        element = None
        if isinstance(rowname, tuple):
            if rowname[0] in tuple_rows_done:
                restriction_type = tuple_rows_done[rowname[0]]
            else:
                restriction_type = E.restriction(base="xs:string")
                tuple_rows_done[rowname[0]] = restriction_type
                element = E.element(
                    E.complexType(
                        E.complexContent(
                            E.extension(
                                E.attribute(
                                    E.annotation(lang("en",E.documentation(
                                        """The type of information reported about this element,
                                        see restriction for details."""
                                    ))),
                                    E.simpleType(
                                        restriction_type
                                    ),
                                    name="type"
                                ),
                                base="informationArea"
                            )
                        ),
                    ),
                    name=rowname[0]
                )
                choice_el.append(element)
            restriction_type.append(E.enumeration(value=rowname[2]))
        elif rowname:
            element = E.element(name=rowname, type="informationArea")
            choice_el.append(element)
        if element is not None and docs[rowx]:
            element.insert(
                0,
                E.annotation(lang("en", E.documentation(docs[rowx])))
            )

def publishingschema(root):
    """ Produce the necessary schema elements for the publishing sheet. 

        root -- an xml element to append to

    """
    global E
    rows = structure.publishing_rows
    docs = structure.publishing_docs
    all_el = E.all()
    root.append(
        E.element(
            E.annotation(lang("en", E.documentation("""
            Contains information about when and how data will be
            published, including any general exceptions.

            All child elements may only contain text, but may also have
            attributes. These may contain short codes - the list these
            codes can be found at http://iati.bjwebb.co.uk/codes.txt

            """))),
            E.complexType(all_el),
            name="publishing"
        )
    )
    for rowx,row in enumerate(rows):
        if row:
            if row[4] == "narrative":
                ext = E.extension(base="narrativeParent")
                el = E.element(
                    E.complexType(
                        E.complexContent(
                            ext
                    ) ),
                    name=row[1],
                    minOccurs="0"
                )
                for i in 2,3:
                    if row[i] != '':
                        if row[i] in structure.date_tags:
                            t = "xs:date"
                        elif row[i] in structure.decimal_tags:
                            t = "xs:decimal"
                        else:
                            t = "xs:string"
                        attribute = E.attribute(name=row[i],
                            type=t)
                        ext.append(attribute)
                        try:
                            attribute.insert(0,
                                E.annotation(lang("en", E.documentation(docs[rowx][i-1])))
                            )
                        except IndexError:
                            pass


            else:
                el = E.element(name=row[1], type="narrativeParent")
            if docs[rowx]:
                if isinstance(docs[rowx], tuple):
                    documentation = docs[rowx][0]
                else:
                    documentation = docs[rowx]
                el.insert(0,
                    E.annotation(lang("en", E.documentation(documentation)))
                )
            all_el.append(el)

def lang(code, el):
    """ Helper function to add language code to an element, since
        Elementmaker syntax does not support namespaces.

    """
    el.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = code
    return el


def full_schema():
    """ Print the full schema, based on the definitions in structure.py"""
    global E
    E = ElementMaker(namespace="http://www.w3.org/2001/XMLSchema",
                     nsmap={'xs':"http://www.w3.org/2001/XMLSchema",
                            'xml':"http://www.w3.org/XML/1998/namespace"})
    headerchoice = E.choice(maxOccurs="unbounded", minOccurs="0")
    root = E.schema(
        # Different syntax to avoid clash with python's import statement
        etree.Element("{http://www.w3.org/2001/XMLSchema}import",
            {'namespace':"http://www.w3.org/XML/1998/namespace",
            'schemaLocation':"xml.xsd"}),
        E.annotation(lang("en", E.documentation("""
        International Aid Transparency Initiative: Implementation
        This file autogenerated {} 

        This W3C XML Schema defines an XML document type for an
        Implementation Schedule of an IATI data provider.

        """.format(datetimestamp())))),
        E.complexType( 
            E.annotation(lang("en", E.documentation("""
            Type that corresponds to a row of the Activity or Organsation
            spreadsheets. Describes the implementation of a specific
            field, or type of information by the data provider.

            Status and exclusion have attributes, containing coded values
            - a list of these codes can be found at
            http://iati.bjwebb.co.uk/codes_activity.txt

            """))),
            headerchoice,
            name = "informationArea"
        ),
        E.element(
            E.annotation(lang("en", E.documentation("""
            Top level element containg elements for each of the top level
            types of information found in the implementation schedule.

            The xml:lang attribute can be used to specify a default
            language for text in the document.

            """))),
            E.complexType(
                E.all(
                    E.element(ref="metadata"),
                    E.element(ref="publishing"),
                    E.element(ref="organisation"),
                    E.element(ref="activity"),
                ),
                E.attribute(ref="xml:lang"),
                E.attribute(
                    E.annotation(lang("en", E.documentation("""
                    The datetime that the xml file was generated.
                    (NOT the date that the schedule was written)
                    """))),
                    name="generated-datetime", type="xs:dateTime")
            ),
            name="implementation"
        ),
        E.element(
            E.annotation(lang("en", E.documentation("""
            Various metadata about the implementation schedule.

            """))),
            E.complexType(
                E.choice(
                    E.element(
                        E.annotation(lang("en", E.documentation("""
                        The publisher that this is a schedule for.
                        The code should be the IATI organisation identifier.
                        
                        """))),
                        name="publisher", type="codeType"),
                    E.element(
                        name="version", type="textType"),
                    E.element(
                        E.annotation(lang("en", E.documentation("""
                        The date when the implementation schedule was last updated.

                        """))),
                        name="date", type="xs:date"),
                    minOccurs="0", maxOccurs="unbounded"
                ),
            ),
            name="metadata"
        ),
        E.element(
            E.annotation(lang("en", E.documentation("""
            Element for enclosing long pieces of human readable text, in
            order to allow multiple translations whilst retaining the
            uniqueness of the parent object.

            """))),
            type="textType",
            name="narrative"
        ),
        E.complexType(
            E.annotation(lang("en", E.documentation("""
            Type for elements that may contain one or more narrative
            elements. Thus this element can be unique, and contain text
            in multiple languages. 

            """))),
            E.choice(
                E.element(ref="narrative"),
                maxOccurs="unbounded",
                minOccurs="0"
            ),
            name="narrativeParent"
        ),
        E.complexType(
            E.annotation(lang("en", E.documentation("""
            Type for elements that contain a string, but also have a code
            attribute. 

            """))),
            E.simpleContent(
                E.extension(
                    E.attribute(name="code", type="xs:string"),
                    base="textType"
                )
            ),
            name="codeType"
        ),
        E.complexType(
            E.annotation(lang("en", E.documentation("""
            Type for elements containing human readable text. Supports
            the xml:lang attribute in order to indicate the language of
            the text. Any element of this type should be repeatable in
            order to provide multiple translations within one xml
            document.

            If no language is indicated, the value specified by the root
            element is used.

            """))),
            E.simpleContent(
                E.extension(
                    E.attribute(ref="xml:lang"),
                    base="xs:string"
                )
            ),
            name="textType"
        )
    )
    for heading in structure.header:
        if heading == '': continue
        if heading in structure.codes_activity: 
            complexType = E.complexType( 
                E.attribute(name="category", type="xs:string")
            )
            if heading == 'exclusions':
                complexType.append( E.choice(
                    E.element(name="narrative",
                              type="textType"),
                    maxOccurs="unbounded"
                ) )
            headerchoice.append(
                E.element( 
                    complexType,
                    name=heading
                ),
            )
        else:
            if heading in structure.date_tags:
                t = "xs:date"
            else:
                t = "textType"
            headerchoice.append(E.element(name=heading, type=t,
                                                minOccurs="0"))
    sheetschema(root, 'organisation')
    sheetschema(root, 'activity')
    publishingschema(root)
    return root

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--schema":
            xml = full_schema()
        else:
            xml = full_xml(sys.argv[1])
        print etree.tostring(xml,
                             pretty_print=True,
                             xml_declaration=True,
                             encoding="utf-8")
    else:
        print """Usage:
        python toxml.py --schema    -- Generates the XML schema 
        python toxml.py [filename]  -- Assumes the file is xls and tries
                                       to generate xml from it"""
