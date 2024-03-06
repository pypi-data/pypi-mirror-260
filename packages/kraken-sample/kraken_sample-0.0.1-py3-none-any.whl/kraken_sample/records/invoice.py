
import datetime
from .organization import organization
from .lorem import lorem
from .order import order


def invoice(id=1):

    record = {
        "@type": "invoice",
        "@id": "test_invoice_id_" + str(id),
        "accountId": "account_avc_123",
        "billingPeriod": "2007-03-01T13:00:00Z/2008-05-11T15:30:00Z",
        "confirmationNumber": "conf_123",
        "customer": organization(1), 
        "description": lorem(),
        "minimumPaymentDue": {
            "@type": "monetaryAmount",
            "currency": "CAD",
            "value": "123.12"
        },
        "name": "order name " + str(id),
        "paymentStatus": "PaymentDue",
        "paymentDueDate": datetime.datetime(2023, 6,1),
        "provider": organization(2),
        "referencesOrder": order(1),
        "scheduledPaymentDate": datetime.datetime(2023, 6,1),
        "totalPaymentDue": {
            "@type": "monetaryAmount",
            "currency": "CAD",
            "value": "1232.21"
        },
    }

    return record

