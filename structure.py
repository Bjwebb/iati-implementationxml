header = ['','','', 'status', 'publication-date', 'exclusion', '', 'provider-definition', 'notes']

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
    ('transcation', 'type', 'reimbursement'),
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

date_tags = [ 'publication-date', 'date-initial', 'date-full' ]
codes = {
        'status': { 'NO':'N', 'PARTIAL':'P', 'YES':'Y' },
        'yesno': { 'Yes': 'y', 'No': 'n' }
    }

codes = {   
    # Data quality
    'quality': {   'Unverified': 'u', 'Verified': 'v'},
    # Exclusions
    'exclusion': {    'a) Not applicable to organisation': 'a',
                      'b) A non-disclosure policy': 'b',
                      'c) Not currently captured and prohibitive cost': 'c',
                      'd) Other': 'd'},
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
    # RAG
    'UNUSED2': {   'Fully compliant': 'fc',
               'Future publication': 'fp',
               'Partially compliant': 'pc',
               'Unable to publish': 'up',
               'Under consideration': 'uc'},
    # Segmentation
    'segmentation': {   'By country / region': 'b',
                        'Other': 'o',
                        'Single file': 's'},
    # Staff resource
    'UNUSED3': { 'Ad hoc': 'a',
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

