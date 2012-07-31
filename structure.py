header = ['','', '', 'status', 'publication-date', 'exclusion', '', 'provider-definition', 'notes']
#header = header[1:]
organisation_rows = ['','','','','','','', 'total-budget', 'recipient-org-budget', 'recipient-country-budget', 'documents'] 
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
    ('title', 'lang', 'agency'), # Ideally bunch these up?
    ('title', 'lang', 'recipient' ),
    ('description', 'lang', 'agency'),
    ('description', 'lang', 'recipient'),
    'activity-status',
    ('activity-date', 'type', 'start'),
    ('activity-date', 'type', 'end'),
    'contact-info',
    ('participating-org', 'role', 'Funding'),
    ('praticipating-org', 'role', 'Extending'),
    ('participating-org', 'role', 'Implementing'),
    ('participating-org', 'role', 'Accountable'),
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
    ('transaction', 'type', 'c'),
    ('transaction', 'type', 'd'),
    ('transcation', 'type', 'r'),
    ('transaction', 'type', 'f'),
    ('transaction', 'type', 'r'),
    '', #Related Documents',
    'document-link',
    'activity-website',
    'related-activity',
    '', #Performance',
    ('conditions', 'info', 'yn'),
    ('conditions', 'info', 'text'),
    'result'
]

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
    ('', 'publication-lifecyle', 'status', '', 'narrative'), #LIFECYCLE
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

date_tags = [ 'publication-date', 'date-initial', 'date-full' ]
codes = {
        'status': { 'NO':'N', 'PARTIAL':'P', 'YES':'Y' },
        'yesno': { 'Yes': 'y', 'No': 'n' }
    }
