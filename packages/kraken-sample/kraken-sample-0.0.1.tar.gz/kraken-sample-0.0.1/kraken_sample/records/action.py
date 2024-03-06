
import datetime

from .organization import organization
from .person import person
from .lorem import lorem
from .order import order
from .product import product

def action(id):
    record = {
        "@type": "action",
        "@id": "test_action_id_" + str(id),
        "name": "test action id " + str(id),
        "description": lorem(),
        "startTime": datetime.datetime(2023, 2, 22),
        "endTime": datetime.datetime(2023, 2, 24),
        "object": order(1),
        "agent": person(1),
        "instrument": product(1),
        "actionStatus": "completedActionStatus",
        "result": [
            product(2),
            product(3),
            product(4),
            product(5)
        ],
        "hasPart": [
            {
                "@type": "action",
                "@id": "test_action_id_" + str(id + 1),
                "name": "test action id " + str(id + 1),
                "description": lorem(),
                "startTime": datetime.datetime(2023, 2, 22),
                "endTime": datetime.datetime(2023, 3, 24),
                "object": order(1),
                "agent": person(1),
                "instrument": product(1),
                "actionStatus": "completedActionStatus"
            },
            {
                "@type": "action",
                "@id": "test_action_id_" + str(id + 2),
                "name": "test action id " + str(id + 2),
                "description": lorem(),
                "startTime": datetime.datetime(2023, 3, 22),
                "endTime": datetime.datetime(2023, 4, 24),
                "object": order(1),
                "agent": person(1),
                "instrument": product(1),
                "actionStatus": "completedActionStatus"
            },
            {
                "@type": "action",
                "@id": "test_action_id_" + str(id + 3),
                "name": "test action id " + str(id + 3),
                "description": lorem(),
                "startTime": datetime.datetime(2023, 4, 22),
                "endTime": datetime.datetime(2023, 5, 24),
                "object": order(1),
                "agent": person(1),
                "instrument": product(1),
                "actionStatus": "completedActionStatus"
            },
            {
                "@type": "action",
                "@id": "test_action_id_" + str(id + 4),
                "name": "test action id " + str(id+ 4),
                "description": lorem(),
                "startTime": datetime.datetime(2023, 5, 22),
                "endTime": datetime.datetime(2023, 6, 24),
                "object": order(1),
                "agent": person(1),
                "instrument": product(1),
                "actionStatus": "completedActionStatus"
            },
            {
                "@type": "action",
                "@id": "test_action_id_" + str(id + 5),
                "name": "test action id " + str(id +5),
                "description": lorem(),
                "startTime": datetime.datetime(2023, 6, 22),
                "endTime": datetime.datetime(2023, 8, 24),
                "object": order(1),
                "agent": person(1),
                "instrument": product(1),
                "actionStatus": "completedActionStatus"
            }
            
        ]
        
    }

    return record
