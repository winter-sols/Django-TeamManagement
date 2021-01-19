CLIENT_TYPE_INDIVIDUAL = 1
CLIENT_TYPE_COMPANY = 2

CLIENT_TYPES = [
    (CLIENT_TYPE_INDIVIDUAL, 'Individual'),
    (CLIENT_TYPE_COMPANY, 'Company')
]

PROJECT_TYPE_BUDGET = 1
PROJECT_TYPE_HOURLY_FT = 2
PROJECT_TYPE_HOURLY_PT = 3
PROJECT_TYPE_CONTRACT = 4

PROJECT_TYPES = [
    (PROJECT_TYPE_BUDGET, 'Budget'),
    (PROJECT_TYPE_HOURLY_FT, 'Hourly FT'),
    (PROJECT_TYPE_HOURLY_PT, 'Hourly PT'),
    (PROJECT_TYPE_CONTRACT, 'Contract'),
]

PROJECT_STATUS_ONGOING = 1
PROJECT_STATUS_PAUSED = 2
PROJECT_STATUS_ENDED = 3

PROJECT_STATUS = [
    (PROJECT_STATUS_ONGOING, 'Ongoing'),
    (PROJECT_STATUS_PAUSED, 'Paused'),
    (PROJECT_STATUS_ENDED, 'Ended'),
]

FINANCIAL_TYPE_SND_INVOICE = 1
FINANCIAL_TYPE_SND_PAYMENT = 2
FINANCIAL_TYPE_DIR_PAYMENT = 3

FINANCIAL_TYPES = [
    (FINANCIAL_TYPE_SND_INVOICE, 'Send Invoice'),
    (FINANCIAL_TYPE_SND_PAYMENT, 'Send Payment'),
    (FINANCIAL_TYPE_DIR_PAYMENT, 'Direct Invoice'),
]

FINANCIAL_STATUS_PENDING = 1
FINANCIAL_STATUS_APPROVED = 2
FINANCIAL_STATUS_DECLINED = 3
FINANCIAL_STATUS_CANCELED = 4

FINANCIAL_STATUS = [
    (FINANCIAL_STATUS_PENDING, 'Pending'),
    (FINANCIAL_STATUS_APPROVED, 'Approved'),
    (FINANCIAL_STATUS_DECLINED, 'Declined'),
    (FINANCIAL_STATUS_CANCELED, 'Canceled')
]