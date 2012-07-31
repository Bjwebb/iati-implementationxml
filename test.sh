#python toxml.py > test.xml 
#python toxml.py test > test.xsd
#xmllint --schema test.xsd test.xml  --noout

for f in schedules/*.xls; do python toxml.py "$f" > xml/tmp.xml; mv xml/tmp.xml "xml/`basename "$f" xls`xml"; done


