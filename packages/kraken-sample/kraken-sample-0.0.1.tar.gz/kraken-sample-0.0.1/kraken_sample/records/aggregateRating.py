
import datetime


def aggregateRating(id):
    record = {
        "@type": "aggregateRating",
        "@id": "agg_1",
        "ratingValue": id,
        "ratingCount": id * 221
    }
    return record
