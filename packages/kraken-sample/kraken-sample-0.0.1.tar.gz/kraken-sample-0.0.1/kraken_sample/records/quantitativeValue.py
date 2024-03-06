def quantitativeValue(id):
    record = {
        "@type": "quantitativeValue",
        "@id": "quant_" + str(id),
        "value": id,
        "unitCode": "cm",
        "unitText": "centimeters"
    }
    return record

