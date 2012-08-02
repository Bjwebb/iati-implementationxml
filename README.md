IATI Implementation Schedule XML generator
==========================================

This code generates XML files for IATI Implementation Schedules
that are in the XLS (Microsoft Excel) format. It can also be used
to produce a schema to validate such XML files against.

Quick Start
-----------

If you haven't already, clone the git repository

    git clone https://github.com/Bjwebb/iati-implementationxml.git
    cd iati-implementationxml

Install the required python dependencies. E.g. on Debian, run:

    sudo aptitude install python-lxml python-xlrd python-parsedatetime

Then

    wget "http://iati.bjwebb.co.uk/schedules.tar.gz"
    tar -xvzf schedules.tar.gz
    mkdir xml
    cd xml
    wget "http://www.w3.org/2009/01/xml.xsd"
    cd ..
    ./test.sh

The xml directory should then have several validating xml files, and
a corresponding schema.

More Options
------------

Run `python toxml.py` for a list of commandline options.
