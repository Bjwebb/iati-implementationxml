IATI Implementation Schedule XML generator
==========================================

This code generates XML files from IATI Implementation Schedules in the
XLS (Microsoft Excel) format, that follow [this
template](http://www.aidtransparency.net/wp-content/uploads/2011/04/IATI-Implementation-Schedule-TEMPLATE.xls).
It can also be used to produce a schema to validate such XML files
against.

Sample output can be found at http://iati.bjwebb.co.uk/xml/

Quick Start
-----------

These instructions assume a unix-like system with git installed.

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
    ./batch.sh

The xml/ directory should then have several validating xml files, and
a corresponding schema.

More Options
------------

Run `python toxml.py` for a list of command-line options for processing single files.

Schema
------

A copy of the schema produced can be found at http://iati.bjwebb.co.uk/xml/implementation.xsd

The schema closely follows the structure of the spreadsheets, with each of the children of the root element corresponding to a single sheet. For the most part, the children of these elements correspond to rows, whose children or attributes then correspond to cells.

The schema contains inline documentation. In addition, an auto-extracted HTML version can be found at http://iati.bjwebb.co.uk/doc/

If you wish to generate the documentation yourself, you need [xs3p](http://xml.fiforms.org/xs3p/). See doc.sh for an example of usage.

