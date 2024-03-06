
import datetime

from .organization import organization
from .imageObject import imageObject

def person(id=1):
    record = {
        "@type": "person",
        "givenName": "Bob" + str(id),
        "familyName": "Smith" + str(id),
        "email": "bob" + str(id) + "@test.com",
        "worksFor": organization(1),
        "jobTitle": "Associate analyst",
        "image": imageObject(id),
        "address": {
            "@type": "postalAddress",
            "streetAddress": "123 Main st.",
            "addressLocality": "Montreal",
            "addressRegion": "QC",
            "addressCountry": "CA",
            "postalCode": "G1G 1G2"
        }
    }
    return record
