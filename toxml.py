import xlrd
from lxml.builder import ElementMaker
import lxml.etree as etree
import datetime
book = xlrd.open_workbook("schedules/Sweden Implementation Schedule.xls")
#book = xlrd.open_workbook("IDB-Implementation-Schedule.xls")
#book = xlrd.open_workbook("IATI-Implementation-Schedule-TEST.xls")
#book = xlrd.open_workbook("IATI-Implementation-Schedule-TEMPLATE.xls")

import structure

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
            rowxml = etree.Element(rowname[0],
                                    {rowname[1]:rowname[2]})
        else:
            rowxml = etree.Element(rowname)
        for colx, heading in enumerate(structure.header):
            if heading == '': continue
            try: cell = sheet.cell_value(rowx=rowx, colx=colx)
            except IndexError: continue
            #if heading == 'exlusion':
            #    cell = sheet.cell_value(rowx=rowx, colx=colx)
            #print rowname, heading, ": ", cell
            if cell:
                a = etree.SubElement(rowxml, heading)
                if heading in structure.date_tags:
                    cell = datetime.datetime(*xlrd.xldate_as_tuple(cell, book.datemode))
                a.text = unicode(cell)
        root.append(rowxml)
    return root

def parse_information(root, sheet, rows):
    for rowx,row in enumerate(rows):
        if row:
            el = etree.SubElement(root, row[1])
            row_data = sheet.row(rowx)
            if row[4] == 'narrative':
                for i in 2,3:
                    if row[i] != '':
                        if row[i] in structure.date_tags and row_data[i].value !='':
                            el.attrib[row[i]] = unicode(datetime.datetime(*xlrd.xldate_as_tuple(row_data[i].value, book.datemode)))
                        else:
                            el.attrib[row[i]] = unicode(row_data[i].value)
                el.text = row_data[4].value
            else:
                el.text = "".join(map(lambda x: x.value, row_data[2:4]))
                
    return root
    

def silent_value(sheet, **args):
    try:
        return sheet.cell_value(**args)
    except IndexError:
        return ''

def full_xml():
    E = ElementMaker()
    sheet = book.sheet_by_index(0)
    root = E.implementation(
        E.metadata(
            E.publisher(
                silent_value(sheet, rowx=2, colx=3),
                code=silent_value(sheet, rowx=4, colx=3)
            ),
            E.version(silent_value(sheet, rowx=7, colx=3)),
            E.date(silent_value(sheet, rowx=7, colx=6))
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

def sheetschema(root, sheet):
    rows = vars(structure)[sheet+'_rows'] 
    tuple_rows_done = []
    E = ElementMaker(namespace="http://www.w3.org/2001/XMLSchema")
    choice = E.choice(maxOccurs="unbounded")
    root.append(
        E.element(E.complexType(choice), name=sheet)
    )
    for rowx,rowname in enumerate(rows):
        if isinstance(rowname, tuple):
            if rowname[0] in tuple_rows_done:
                continue
            else:
                tuple_rows_done.append(rowname[0])
            root.append( E.element(
                E.complexType( E.complexContent(
                    E.extension(
                        E.attribute(name=rowname[1], type="xs:string", use="required"), 
                        base="informationArea",
                    )
                ) ),
                name = rowname[0]
            ) ) 
            choice.append( E.element(ref=rowname[0]) )
        else:
            if rowname == '':
                continue
            root.append( E.element(
                type = "informationArea",
                name = rowname
            ) )
            choice.append( E.element(ref=rowname) )

def publishingschema(root):
    rows = structure.publishing_rows
    E = ElementMaker(namespace="http://www.w3.org/2001/XMLSchema")
    choice = E.choice(maxOccurs="unbounded")
    root.append(
        E.element(E.complexType(choice), name="publishing")
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
                    name=row[1]
                )
                for i in 2,3:
                    if row[i] != '':
                        ext.append( E.attribute(name=row[i], type="xs:string") )
            else:
                el = E.element(name=row[1], type="xs:string")
            choice.append(el)

import sys
if len(sys.argv) > 1:
    mode = sys.argv[1]
    E = ElementMaker(namespace="http://www.w3.org/2001/XMLSchema")
    headerchoice = E.all()
    root = E.schema(
        E.complexType( 
            headerchoice,
            name = "informationArea"
        ),
        E.element(
            E.complexType(
                E.all(
                    E.element(
                        E.complexType(
                            E.all(
                                E.element(
                                    E.complexType(
                                        E.simpleContent(
                                            E.extension(
                                                E.attribute(name="code", type="xs:string"),
                                                base="xs:string"
                                            )
                                        )
                                    ),
                                    name="publisher"
                                ),
                                E.element(name="version", type="xs:string"),
                                E.element(name="date", type="xs:string")
                            ),
                        ),
                        name="metadata"
                    ),
                    E.element(ref="publishing"),
                    E.element(ref="organisation"),
                    E.element(ref="activity"),
                )
            ),
            name="implementation"
        )
    )
    for heading in structure.header:
        if heading == '': continue
        ## Use of xs: here, FIXME
        headerchoice.append( E.element(name=heading, type="xs:string", minOccurs="0") )
    sheetschema(root, 'organisation')
    sheetschema(root, 'activity')
    publishingschema(root)
    print '<?xml version="1.0" encoding="utf-8"?>'
    print(etree.tostring(root, pretty_print=True))

else:
    full_xml()

    
"""
sheet = book.steet_by_index(3)
test = []
for i in xrange(0,sheet.nrows):
    print "'"+sheet.cell_value(rowx=i, colx=1)+"',"
    """
