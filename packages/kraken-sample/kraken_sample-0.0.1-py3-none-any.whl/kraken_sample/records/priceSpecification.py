
import datetime

def priceSpecification(id=1):
    record = {
        "@type": "priceSpecification",
        "@id": "price_" + str(id),
        "price": round(id * 100 /1.0775, 2),
        "priceCurrency": "CAD",
        "valueAddedTaxIncluded": False
    }
    return record



def priceSpecification_tax(id=1, name='gst', rate=0.07):
    record = {
        "@type": "priceSpecification",
        "@id": "price_" + str(id),
        "name": name,
        "price": round((id * 100 /1.0775) * rate, 2),
        "priceCurrency": "CAD",
        "valueAddedTaxIncluded": True
    }
    return record
