
import datetime

def organization(id=1):

    record = {
        "@type": "organization",
        "@id": "test_org_id" + str(id), 
        "name": "ACME" + str(id),
        "email": "info" + str(id) + "@acme.com",
        "url": "https://www.acme" + str(id) + ".com",
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
