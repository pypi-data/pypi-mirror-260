
import datetime


from .organization import organization
from .person import person
from .lorem import lorem


def article(id):
    
    record = {
        "@type": "article",
        "@id": "article_" + str(id),
        "name": "article_" + str(id),
        "headline": "Article headline " + str(id),
        "abstract": lorem(),
        "text": lorem(),
        "author": person(1),
        "datePublished": datetime.datetime(2023,12,22),
        "contentUrl": "/image.png",
        "hasPart": [
            {
                "@type": "article",
                "@id": "sub_article_" + str(1),
                "name": "sub_article_" + str(1),
                "headline": "Sub Article headline " + str(1),
                "text": lorem(),
            },
            {
                "@type": "article",
                "@id": "sub_article_" + str(2),
                "name": "sub_article_" + str(2),
                "headline": "Sub Article headline " + str(2),
                "text": lorem(),
            },
            {
                "@type": "article",
                "@id": "sub_article_" + str(3),
                "name": "sub_article_" + str(3),
                "headline": "Sub Article headline " + str(3),
                "text": lorem(),
            }
            
        ]
    }
    return record

