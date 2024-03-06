
import datetime
from .lorem import lorem

from .priceSpecification import priceSpecification, priceSpecification_tax
from .product import product

def order_item(id=1):
    record = {
        "@type": "orderItem",
        "@id": "orderItem_" + str(id),
        "orderedItem": product(id),
        "orderItemNumber": id,
        "orderQuantity": id * 2,
        "description": lorem(),
        "price": [
            priceSpecification(id),
            priceSpecification_tax(id, 'gst', 0.07),
            priceSpecification_tax(id, 'qst', 0.065)
        ]
    }
    return record
