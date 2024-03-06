
import datetime



def rating(id):
    record = {
        "@type": "rating",
        "@id": "test_rating_id_" + str(id),
        "ratingValue": id,
        "ratingAspect": "rating aspect"
    }

    return record

