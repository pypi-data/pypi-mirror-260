
import datetime



def website(id):
    
    record = {
        "@type": "WebSite",
        "name": "Test01",
        "image": "alarm",
        "date": datetime.datetime(2024,1,1),
        "url": "https://www.test.com",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        "contentUrl": "/image.png",
        "deliveryAddress": {
            "@type": "postalAddress",
            "streetAddress": "123 Main st.",
            "addressLocality": "Montreal",
            "addressRegion": "QC",
            "addressCountry": "CA",
            "postalCode": "G1G 1G2"
        },
        "customer": {
            "@type": "person",
            "givenName": "Bob",
            "familyName": "Smith",
            "email": "bob@test.com",
            "address": {
                "@type": "postalAddress",
                "streetAddress": "123 Main st.",
                "addressLocality": "Montreal",
                "addressRegion": "QC",
                "addressCountry": "CA",
                "postalCode": "G1G 1G2"
            },
        },
        "price": {
            "@type": "priceSpecification",
            "priceCurrency": "USD",
            "price": 45.95
        },
        "quantity": {
            "@type": "quantitativeValue",
            "value": 23.5,
            "unitCode": 'EA'
        },
        "potentialAction": [
            {
                "@type": "action",
                "name": "Home",
                "url": "/",
                "contentUrl": "/image.png"
            },
            {
                "@type": "action",
                "name": "User",
                "url": "/user",
                "contentUrl": "/image.png"
            }
        ],
        "hasPart": [
            {
                "@type": "webpage",
                "name": "Home",
                "url": "/",
                "contentUrl": "/image.png"
            },
            {
                "@type": "webpage",
                "name": "Terms and conditions",
                "url": "/terms",
                "contentUrl": "/image.png"
            },
            {
                "@type": "webpage",
                "name": "Privacy policy",
                "url": "/privacy",
                "contentUrl": "/image.png"
            },
            {
                "@type": "webpage",
                "name": "Contact us",
                "url": "/contact",
                "contentUrl": "/image.png"
            }
    
        ]
    
    }
    return record

