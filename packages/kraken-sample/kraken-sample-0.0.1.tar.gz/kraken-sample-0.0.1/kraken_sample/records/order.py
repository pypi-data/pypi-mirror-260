
import datetime
from .organization import organization
from .person import person
from .lorem import lorem
from .order_item import order_item
from .postalAddress import postalAddress

def order(id=1):

    record = {
        "@type": "order",
        "@id": "test_order_id_" + str(id),
        "orderNumber": "abc123",
        "name": "order name " + str(id),
        "orderDate": datetime.datetime(2023, 12, 22),
        "customer": organization(1),
        "seller": organization(2),
        "billingAddress": postalAddress(1),
        "orderStatus": "OrderInTransit",
        "orderedItem": [
            order_item(1),
            order_item(2),
            order_item(3),
            order_item(4),
            order_item(5),
            order_item(6)
        ]
    }

    return record

