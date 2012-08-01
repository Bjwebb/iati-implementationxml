import xlrd
from lxml.builder import ElementMaker
import lxml.etree as etree
import datetime

import structure

datemode = None
def get_date(value):
    """ Helper function to return the xml date string for a given
        spreadsheet cell value.
    
    """
    global datemode
    try:
        date = datetime.datetime(*xlrd.xldate_as_tuple(value, datemode))
        return unicode(date)
    except ValueError:
        return ''

def use_code(heading, text):
    """ Helper function to return the short code for a given heading
        and text value.

    """
    if heading in structure.codes:
        if text == '': return ''
        return structure.codes[heading][text]
    else:
        return text


def parse_data(root, sheet, rows):
    """ Parse a 'data' sheet.
        ie. Activity Data or Organisation Data

        root -- an xml element to append to
        sheet -- the xlrd sheet element to parse
        rows -- a list of xml tags that correspond to each row
        
    """
    tuple_rows_done = {}
    for rowx,rowname in enumerate(rows):
        if rowname == '':
            continue
        if isinstance(rowname, tuple):
            if rowname[0] in tuple_rows_done:
                subroot = tuple_rows_done[rowname[0]]
            else:
                subroot = etree.SubElement(root, rowname[0])
                tuple_rows_done[rowname[0]] = subroot
            rowxml = etree.SubElement(subroot, rowname[2])
        else:
            rowxml = etree.SubElement(root, rowname)
        
        for colx, heading in enumerate(structure.header):
            if heading == '':
                continue
            try:
                cell = sheet.cell_value(rowx=rowx, colx=colx)
            except IndexError:
                continue
            el = etree.SubElement(rowxml, heading)
            if heading in structure.date_tags:
                cell = get_date(cell)
            else:
                cell = unicode(cell)
            if cell != '':
                el.text = cell
            if heading == 'exclusion':
                try:
                    next_cell = unicode(sheet.cell_value(rowx=rowx, colx=colx+1))
                    if next_cell == '':
                        continue
                    else:
                        el.attrib['code'] = use_code(heading,
                                                unicode(next_cell))
                except IndexError:
                    continue
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
            row_data = sheet.row(rowx)
            if row[4] == 'narrative':
                for i in 2,3:
                    if row[i] != '':
                        if row[i] in structure.date_tags and row_data[i].value !='':
                            el.attrib[row[i]] = get_date(row_data[i].value)
                        else:
                            el.attrib[row[i]] = use_code(row[i],
                                    unicode(row_data[i].value))
                el.text = row_data[4].value
            else:
                el.text = "".join(map(lambda x: x.value, row_data[2:4]))
                
    return root
    

def silent_value(sheet, **args):
    """ Helper function to fetch cell values and convert them to strings,
        whilst ignoring possible exceptions.

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
    root = E.implementation(
        E.metadata(
            E.publisher(
                silent_value(sheet, rowx=2, colx=6),
                code=silent_value(sheet, rowx=4, colx=6)
            ),
            E.version(silent_value(sheet, rowx=6, colx=3)),
            E.date(silent_value(sheet, rowx=6, colx=6)) # TODO Add handling of proper excel dates
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
    )
    print '<?xml version="1.0" encoding="utf-8"?>'
    print(etree.tostring(root, pretty_print=True))


def sheetschema(root, sheetname):
    """ Produce the schema elements for the named sheet.

        root -- an xml element to append to
        sheetname -- the short name of a sheet, as used in the structure
                     data and as the xml tag name.
                     Possible values are 'activity' and 'organisation'

    """
    global E
    rows = vars(structure)[sheetname+'_rows'] 
    tuple_rows_done = {}
    all_el = E.all()
    root.append(
        E.element(E.complexType(all_el), name=sheetname)
    )
    for rowx,rowname in enumerate(rows):
        if isinstance(rowname, tuple):
            if rowname[0] in tuple_rows_done:
                suball = tuple_rows_done[rowname[0]]
            else:
                suball = E.all()
                all_el.append( E.element(
                    E.complexType(suball),
                    name = rowname[0],
                    minOccurs="0"
                ) )
                tuple_rows_done[rowname[0]] = suball 
            suball.append( E.element(
                type = "informationArea",
                name = rowname[2],
                minOccurs="0"
            ) )
        else:
            if rowname == '':
                continue
            all_el.append( E.element(
                type = "informationArea",
                name = rowname,
                minOccurs="0"
            ) )


def publishingschema(root):
    """ Produce the necessary schema elements for the publishing sheet. 

        root -- an xml element to append to

    """
    global E
    rows = structure.publishing_rows
    all_el = E.all()
    root.append(
        E.element(E.complexType(all_el), name="publishing")
    )
    for rowx,row in enumerate(rows):
        if row:
            if row[4] == "narrative":
                ext = E.extension(base="xs:string")
                el = E.element(
                    E.complexType(
                        E.simpleContent(
                            ext
                    ) ),
                    name=row[1],
                    minOccurs="0"
                )
                for i in 2,3:
                    if row[i] != '':
                        ext.append( E.attribute(
                            name=row[i],
                            type="xs:string") )
            else:
                el = E.element(name=row[1], type="xs:string",
                                                    minOccurs="0")
            all_el.append(el)


def full_schema():
    """ Print the full schema, based on the definitions in structure.py"""
    global E
    E = ElementMaker(namespace="http://www.w3.org/2001/XMLSchema",
                     nsmap={'xs':"http://www.w3.org/2001/XMLSchema"})
    headerall = E.all()
    root = E.schema(
        E.complexType( 
            headerall,
            name = "informationArea"
        ),
        E.element(
            E.complexType(
                E.all(
                    E.element(ref="metadata"),
                    E.element(ref="publishing"),
                    E.element(ref="organisation"),
                    E.element(ref="activity"),
                )
            ),
            name="implementation"
        ),
        E.element(
            E.complexType(
                E.all(
                    E.element(name="publisher", type="codeType",
                                    minOccurs="0"),
                    E.element(name="version", type="xs:string",
                                    minOccurs="0"),
                    E.element(name="date", type="xs:string",
                                    minOccurs="0")
                ),
            ),
            name="metadata"
        ),
        E.complexType(
            E.simpleContent(
                E.extension(
                    E.attribute(name="code", type="xs:string"),
                    base="xs:string"
                )
            ),
            name="codeType"
        ),
    )
    for heading in structure.header:
        if heading == '': continue
        if heading == 'exclusion':
            t = 'codeType'
        else:
            t = 'xs:string'
        headerall.append(E.element(name=heading, type=t, minOccurs="0"))
    sheetschema(root, 'organisation')
    sheetschema(root, 'activity')
    publishingschema(root)
    print '<?xml version="1.0" encoding="utf-8"?>'
    print(etree.tostring(root, pretty_print=True))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--schema":
            full_schema()
        else:
            full_xml(sys.argv[1])
    else:
        print """Usage:
        python toxml.py --schema    -- Generates the XML schema 
        python toxml.py [filename]  -- Assumes the file is xls and tries
                                       to generate xml from it"""
