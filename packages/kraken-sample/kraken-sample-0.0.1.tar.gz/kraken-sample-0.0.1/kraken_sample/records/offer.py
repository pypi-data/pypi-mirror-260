
from .priceSpecification import priceSpecification


def offer(id):
    record = {
        "@type": "offer",
        "@id": "offer_" + str(id),
        "priceSpecification": priceSpecification(id),
        "url": 'https://www.test.com',
        "potentialAction": [
            {'@type': "action", "@id": "buy_now", "name": "Buy now", "url":"https://www.test.com"}
        ]
    }
    return record
