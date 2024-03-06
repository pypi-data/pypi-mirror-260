
import datetime


from .lorem import lorem
from .person import person
from .rating import rating

def review(id):

    record = {
        "@type": "review",
        "@id": "test_review_id_" + str(id),
        "author": person(1),
        "reviewRating": rating(id),
        "headline": "Headline of the review",
        "reviewAspect": "Aspect of the review",
        "reviewBody": lorem(),
        "datePublished": datetime.datetime(2023, 3, 28),
        "positiveNotes": [
            "positive note 1",
            "positive note 2",
            "positive note 3",
            "positive note 4"
        ],
        "negativeNotes": [
            "negative note 1",
            "negative note 2",
            "negative note 3",
            "negative note 4"
        ]
    }

    return record
