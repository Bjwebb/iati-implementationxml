#python toxml.py > test.xml 
#python toxml.py test > test.xsd
#xmllint --schema test.xsd test.xml  --noout

for f in schedules/*.xls; do
    echo "Processing $f"
    python toxml.py "$f" > xml/tmp.xml;
    mv xml/tmp.xml "xml/`basename "$f" xls`xml";
done
echo
python toxml.py --schema > xml/implementation.xsd
for f in xml/*.xml; do
    xmllint --schema xml/implementation.xsd "$f" --noout;
done


