
import datetime

from .aggregateRating import aggregateRating
from .brand import brand
from .imageObject import imageObject
from .lorem import lorem
from .offer import offer
from .organization import organization
from .quantitativeValue import quantitativeValue
from .review import review



def product(id=1):
    record = {
        "@type": "product",
        "@id": "product_" + str(id),
        "name": "product_" + str(id),
        "image": imageObject(id),
        "description": lorem(),
        "model": "ABC123",
        "color": "black",
        "brand": brand(1),
        "manufacturer": organization(1),
        "mpn": "aabbcc112233",
        "width": quantitativeValue(20),
        "height": quantitativeValue(25),
        "depth": quantitativeValue(12),
        "weight": quantitativeValue(200),
        "aggregateRating": aggregateRating(3.7),
        "offers": offer(345.22),
        "review": [
            review(1),
            review(1.5),
            review(3.5),
            review(5)
        ]
    }
    return record
