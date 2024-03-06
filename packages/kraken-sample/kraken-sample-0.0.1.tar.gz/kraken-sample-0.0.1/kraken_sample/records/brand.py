

from .imageObject import imageObject

def brand(id):
    record = {
        "@type": "brand",
        "@id": "brand_1",
        "name": "Brand 1",
        "logo": imageObject(1),
    }
    return record