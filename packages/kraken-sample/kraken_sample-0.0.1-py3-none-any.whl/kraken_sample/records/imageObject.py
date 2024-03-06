





def imageObject(id):
    record = {
        "@type": "imageObject",
        "@id": "image_" + str(id),
        "name": "image_" + str(id),
        "contentUrl": "/image.png"
    }
    return record
