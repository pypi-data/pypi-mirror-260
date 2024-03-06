
    
import copy
from kraken_sample.helpers import json
from kraken_sample.helpers import things
import os
import pkg_resources
import datetime

from kraken_sample.records import records

"""
Notes:
To access files in data directory, use:
new_path = pkg_resources.resource_filename('kraken_sample', old_path)

"""

        
def get(record_type, id=1):
    """
    """
    return records.get(record_type, id)
    
    return True




    
    