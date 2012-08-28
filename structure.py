# This file contains the mapping between the Implementation Schedule
# spreadsheets and the outputted XML files.

# Map of each column of the activity and organisation tables
header = ['','','', 'status', 'publication-date', 'exclusion', '', 'provider-definition', 'notes']


# Map each row in the organisation table to a named XML element
organisation_rows = ['','','','','','','', 'total-budget', 'recipient-org-budget', 'recipient-country-budget', 'document-link'] 

# Documentation for each of these elements
organisation_docs = ['', '', '', '', '', '', '', 'Annual forward planning budget data for agency', 'Annual forward planning budget for funded institutions', 'Annual forward planning budget data for countries', 'Organisation documents']


# Map each row in the activity table to a named XML element
# Either elementname, or (elementname, UNUSED, type)
# Where type is the value that the type attribute will have
activity_rows = [
    '',
    '',
    '',
    '',
    '',
    '',
    '',
    '', #Identification',
    'reporting-org',
    'iati-identifier',
    'other-identifier',
    '', #Basic Activity Information',
    ('title', 'lang', 'agency'),
    ('title', 'lang', 'recipient' ),
    ('description', 'lang', 'agency'),
    ('description', 'lang', 'recipient'),
    'activity-status',
    ('activity-date', 'type', 'start'),
    ('activity-date', 'type', 'end'),
    'contact-info',
    ('participating-org', 'role', 'funding'),
    ('participating-org', 'role', 'extending'),
    ('participating-org', 'role', 'implementing'),
    ('participating-org', 'role', 'accountable'),
    '', #Geopolitical Information',
    'recipient-country',
    'recipient-region',
    'location',
    '', #Classifications',
    ('sector', 'type', 'crs'), # TODO Bring these terms in line with those used in the main XML
    ('sector', 'type', 'agency'),
    'policy-marker',
    'collaboration-type',
    'default-flow-type',
    'default-finance-type',
    'default-aid-type',
    'default-tied-status',
    '', #Financial',
    'budget',
    'planned-disbursement',
    '', #'UNDERDEVELOPMENT-RecipientCountryBudgetIdentifier',
    '', #Financial Transaction',
    ('transaction', 'type', 'commitment'),
    ('transaction', 'type', 'disbursement'),
    ('transaction', 'type', 'reimbursement'),
    ('transaction', 'type', 'incoming'),
    ('transaction', 'type', 'repayment'),
    '', #Related Documents',
    'document-link',
    'activity-website',
    'related-activity',
    '', #Performance',
    ('conditions', 'info', 'attached'),
    ('conditions', 'info', 'text'),
    'result'
]

# Documentation for each of the activity rows
activity_docs = [
    '', 'Activities', '', 'Note: definitions and code lists can be found at:', 'http://iatistandard.org/activities-standard', '', 'Information Area', 'Identification', 'Reporting Organisation', 'IATI activity identifier', 'Other activity identifiers', 'Basic Activity Information', 'Activity Title (Agency language)', 'Activity Title (Recipient language)', 'Activity Description (Agency language)', 'Activity Description (Recipient language)', 'Activity Status', 'Activity Dates (Start Date)', 'Activity Dates (End Date)', 'Activity Contacts', 'Participating Organisation (Funding)', 'Participating Organisation (Extending)', 'Participating Organisation (Implementing)', 'Participating Organisation (Accountable)', 'Geopolitical Information', 'Recipient Country', 'Recipient Region', 'Sub-national Geographic Location', 'Classifications', 'Sector (DAC CRS)', 'Sector (Agency specific)', 'Policy Markers', 'Collaboration Type', 'Default Flow Type', 'Default Finance Type', 'Default Aid Type', 'Default Tied Aid Status', 'Financial', 'Activity Budget', 'Planned Disbursements', '(UNDER DEVELOPMENT) Recipient Country Budget Identifier', 'Financial Transaction', 'Financial transaction (Commitment)', 'Financial transaction (Disbursement & Expenditure)', 'Financial transaction (Reimbursement)', 'Financial transaction (Incoming Funds)', 'Financial transaction (Loan repayment / interest repayment)', 'Related Documents', 'Activity Documents', 'Activity Website', 'Related Activity', 'Performance', 'Conditions attached Y/N', 'Text of Conditions', 'Results data'
]


# Map each row in the publishing table to an element
# And each cell to an attribute or narrative element
# () for unparsed rows, organisations
# ('', 'element for row', 'attribute/narrative', 'attribute/narrative', 'attribute/narrative')
publishing_rows = [
    (),
    (),
    (),
    (),
    (),
    (),
    ('', 'scope', 'value', '', 'narrative'), #SCOPE
    (),
    (),
    ('', 'publication-timetable', 'date-initial', 'date-full', 'narrative'), #TIMETABLE
    (),
    (),
    ('', 'publication-frequency', 'frequency', 'timeliness', 'narrative'), #TIMEFREQ
    (),
    (),
    ('', 'publication-lifecyle', 'point', '', 'narrative'), #LIFECYCLE
    (),
    (),
    ('', 'data-quality', 'quality', '', 'narrative'), #DATAQUAL
    (),
    (),
    ('', 'approach', 'resource', '', 'narrative'), #SYSRESOURCES
    (),
    ('', 'notes', '', '', ''), #NOTES
    (),
    (),
    (),
    (),
    (),
    (),
    ('', 'thresholds', '', '', ''), #THRESH
    (),
    ('', 'exclusions', '', '', ''), #EXCLUSIONS
    (),
    ('', 'constraints-other', '', '', ''), #OTHER
    (),
    (),
    (),
    (),
    (),
    (),
    (),
    ('', 'license', 'license', '', 'narrative'), #LICENCE
    (),
    (),
    ('', 'activity-multilevel', 'yesno', '', 'narrative'), #MULTILEVEL
    (),
    (),
    ('', 'segmentation', 'segmentation', '', 'narrative'), #SEGMENT
    (),
    (),
    ('', 'user-interface', 'status', '', 'narrative') #USERINT
]

# Documentation for each of the publishing rows
# Note that these tuples are misaligned by 1 value from those above
publishing_docs = [
    '',
    '',
    '1. When will data be published?',
    '',
    'Timetable and frequency of publication',
    '',
    ('Which organisations/agencies/programmes will your IATI data cover? (What % of your total development flows does this cover? What is missing?)',
    'Percentage of total budget / ODA'),
    '',
    '',
    ('Overall timetable for publication (Provide a date for when these organisations will publish (a) an initial (incomplete) set of IATI data and (b) full IATI implementation)',
    'Date of initial implementation',
    'Date of full implementation'),
    '',
    '',
    ('Timeliness and frequency of publication (How soon after data is captured and available internally will data be published? How frequently will data be published?)',
    'Frequency of publication',
    'Timeliness of publication'),
    '',
    '',
    ('How early in lifecycle will activity details be published? (Will activity details be published during the pipeline/identification stage or not until they are approved and in the implementation stage)',
    'Lifecycle status at publication'),
    '',
    '',
    ('Data quality status (Do you want to identify the status of the quality/audit/statistical verification of data that is published in registry? Please indicate whether you anticipate doing this, and the likely timing of moving from unverified data to verified data)',
    'Data quality'),
    '',
    '',
    ('Approach to publication (Please outline what staff and system resources are being made available to implement IATI,  any relevant organisational structures e.g. working groups, and who is leading on IATI implementation)',
    'System resource'),
    '',
    'Other notes',
    '',
    '',
    '2. What are the exclusions from publication?',
    '',
    '',
    'Exceptions and constraints: general rules that exclude activities from being published. Any specific data item exclusions should be listed in the data tables (Organisation data tab and Activity data tab).',
    'Thresholds (are there any thresholds on the value of activities or transactions to be published. Please specify what the general threshold limits are for publication)',
    '',
    'Exclusions (Please identify any rules for excluding data or information that will either be applied automatically or used as a basis to manually exclude publication. Note that exceptions for publication should be kept to a minimum and based on existing national or other regulations)',
    '',
    'Any general issues or other constraints',
    '',
    '',
    '3. How will data be published? ',
    '',
    '',
    '',
    '',
    ('Information for prospective users of information',
    'Licensing (Under which license will data be published: public domain or attribution? If the license does not meet the IATI standard please specify why. Please state whether you intend to use the IATI authorised license or another)',
    'Licence type'),
    '',
    '',
    ('Definition of an activity and multi-level activities (How is an activity defined e.g. projects and programmes, or some other structure? Do you have multi-tiered project structures e.g. projects and sub-projects or components? At which level do you intend to publish details (e.g. transactions)?)',
    'Multi-level activities reported?'),
    '',
    '',
    ('Segmenting data for publication (The recommendation is to publish data segmented by country i.e. one data file for each country. Duplicate project data must not exist within different files, so projects targeting multiple countries or regional/worldwide by nature should be held within a non-country specific file(s). Is this a practical suggestion for your programme? How many projects are not specific to one country and what non-country files best suit your programme?)',
    'Segmentation'),
    '',
    '',
    ('Do you intend to provide a user interface in addition to raw IATI data? (Will IATI data be accessible for end users through an existing or a new user interface on your website? [Note: this is not an IATI requirement])',
    'User interface?'),
]


# List of XML elements that will contain a date
date_tags = [ 'publication-date', 'date-initial', 'date-full' ]
# List of XML elements that will contain a decimal value
decimal_tags = [ 'value' ]


# Codes for xml elements named in `header` above
codes_activity = {
    # Status
    'status': {    'Fully compliant': 'fc',
                   'Future publication': 'fp',
                   'Partially compliant': 'pc',
                   'Unable to publish': 'up',
                   'Under consideration': 'uc'},
    # Exclusions
    'exclusions': {    'a) Not applicable to organisation': 'a',
                      'b) A non-disclosure policy': 'b',
                      'c) Not currently captured and prohibitive cost': 'c',
                      'd) Other': 'd'}
}

# Codes for xml elements corresponding to an element from the publishing
# table.
# These were extracted from a hidden row in the excel spreadsheet
# Those named UNUSED and UNUSED2 were found here, but not used in any of
# the main tables.
codes = {   
    # Data quality
    'quality': {   'Unverified': 'u', 'Verified': 'v'},
    # Frequency
    'frequency': {   'Annually': 'a',
                     'Bi-annually': 'b',
                     'Fortnightly': 'f',
                     'Monthly': 'm',
                     'Other': 'o',
                     'Quarterly': 'q',
                     'Real time': 'r',
                     'Weekly': 'w'},
    # License type
    'license': {    'Attribution-only': 'a',
                    'Other (non-compliant)': 'o',
                    'Public domain': 'p'},
    # Lifecyle
    'point': {   'Implementation': 'i',
                 'Other': 'o',
                 'Pipeline/identification': 'p'},
    # Multi-level reporting
    'yesno': {   'No': 'n', 'Yes': 'y'},
    # Multi-level type
    'UNUSED': { 'Both': 'b',
                'Hierarchy': 'h',
                'Related activities': 'r'},
    # Segmentation
    'segmentation': {   'By country / region': 'b',
                        'Other': 'o',
                        'Single file': 's'},
    # Staff resource
    'UNUSED2': {  'Ad hoc': 'a',
                  'Dedicated resource': 'd',
                  'Other': 'o',
                  'Working group': 'w'},
    # System resource
    'resource': {  'Direct feed from internal systems': 'd',
                   'Excel spreadsheet conversion': 'e',
                   'Manual capture through an online tool (web entry platform)': 'm',
                   'Other': 'o'},
    # Timeliness
    'timeliness': {   '1 month in arrears': '1m',
                      '1 quarter in arrears': '1q',
                      '1 week in arrears': '1w',
                      '2 months in arrears': '2m',
                      '2 weeks in arrears': '2w',
                      '> 1 quarter in arrears': 'gt',
                      'Other': 'o',
                      'Real time': 'r'},
    # User interface
    'status': {   'In development': 'i',
                  'No': 'n',
                  'Under consideration': 'u',
                  'Yes': 'y'}}

