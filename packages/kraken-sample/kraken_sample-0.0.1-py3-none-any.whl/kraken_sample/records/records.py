
import datetime
from .action import action
from .article import article
from .invoice import invoice
from .lorem import lorem
from .order_item import order_item
from .order import order
from .organization import organization
from .person import person
from .postalAddress import postalAddress
from .priceSpecification import priceSpecification
from .product import product
from .rating import rating
from .review import review
from .thing import thing
from .website import website


def record_types():

    types = [
        'action', 
        'invoice',
        'order',
        'organization',
        'person',
        'postalAddress',
        'product',
        'order_item',
        'priceSpecification',
        'website',
        'article',
        "rating",
        "review"
    ]
    types = sorted(types)
    return types

def get(record_type, id=1):

    if record_type == 'action':
        return action(id)

    if record_type == 'invoice':
        return invoice(id)
        
    if record_type == 'order':
        return order(id)
        
    if record_type == 'organization':
        return organization(id)

    if record_type == 'person':
        return person(id)
    
    if record_type == 'postalAddress':
        return postalAddress(id)
    
    if record_type == 'product':
        return product(id)

    if record_type == 'order_item':
        return order_item(id)
    
    if record_type == 'priceSpecification':
        return priceSpecification(id)
    
    if record_type == 'website':
        return website(id)

    if record_type == 'article':
        return article(id)
        
    if record_type == 'rating':
        return rating(id)
        
    if record_type == 'review':
        return review(id)
    
    else:
        return thing(id)

