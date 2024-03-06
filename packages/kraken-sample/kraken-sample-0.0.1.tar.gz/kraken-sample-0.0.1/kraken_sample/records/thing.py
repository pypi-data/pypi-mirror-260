
import datetime
from .lorem import lorem
from .imageObject import imageObject

def thing(id):

    record = {
        "@type": "thing",
        "@id": "test_review_id_" + str(id),
        "name": "thing name " + str(id),
        "description": lorem(),
        "url": "https://www.test.com/",
        "image": imageObject(id)
    }

    return record
