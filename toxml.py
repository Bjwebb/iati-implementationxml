import xlrd
from lxml.builder import E
import lxml.etree as etree
import datetime
book = xlrd.open_workbook("IDB-Implementation-Schedule.xls")
#book = xlrd.open_workbook("IATI-Implementation-Schedule-TEST.xls")
#book = xlrd.open_workbook("IATI-Implementation-Schedule-TEMPLATE.xls")

import structure

def parse_data(root, sheet, rows):
    for rowx,rowname in enumerate(rows):
        rowname = rowname.translate(None, " -()/&") #FIXME remove
        if rowname == '': continue
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

def full_xml():
    root = E.implementation(
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
    print(etree.tostring(root, pretty_print=True))


import sys
if len(sys.argv) > 1:
    mode = sys.argv[1]
else:
    full_xml()

    
"""
sheet = book.steet_by_index(3)
test = []
for i in xrange(0,sheet.nrows):
    print "'"+sheet.cell_value(rowx=i, colx=1)+"',"
    """
