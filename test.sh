python toxml.py > test.xml 
python toxml.py test > test.xsd
xmllint --schema test.xsd test.xml  --noout

