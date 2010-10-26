# -*- coding: utf-8 -*-
"""
In this module, we collect functions that are used in the context
of identifiers used in opengem (e.g., memcached keys).
"""

import uuid

DEFAULT_LENGTH_RANDOM_ID = 8
MAX_LENGTH_RANDOM_ID = 36

# using '!' as separator in keys, because it is not used in numbers
MEMCACHE_KEY_SEPARATOR = '!'
INTERNAL_ID_SEPARATOR = ':'

ERF_KEY_TOKEN = 'erf'
SITES_KEY_TOKEN = 'sites'
MGM_KEY_TOKEN = 'mgm'
HAZARD_CURVE_KEY_TOKEN = 'hazard_curve'
EXPOSURE_KEY_TOKEN = 'exposure'
GMF_KEY_TOKEN = 'gmf'
VULNERABILITY_CURVE_KEY_TOKEN = 'vulnerability_curves'

LOSS_RATIO_CURVE_KEY_TOKEN = 'loss_ratio_curve'
LOSS_CURVE_KEY_TOKEN = 'loss_curve'
CONDITIONAL_LOSS_KEY_TOKEN = 'loss_conditional'

def generate_sequence():
    """generator for sequence IDs"""
    counter = 0
    while(True):
        counter += 1
        yield counter

def generate_id(prefix):
    """generator for task IDs (prefix+sequence number)"""
    counter = 0
    while(True):
        counter += 1
        yield INTERNAL_ID_SEPARATOR.join((str(prefix), str(counter)))

def generate_product_key(job_id, product, block_id="", site=""):
    """construct memcached key from several part IDs"""
    # TODO(chris): FIXME modify below to always have 4 fields in the key.

    strip = lambda x: x.replace(" ", "")
    key_list = [str(job_id), str(block_id),
            strip(str(site)), strip(str(product))]

    return MEMCACHE_KEY_SEPARATOR.join(key_list)

def generate_random_id(length=DEFAULT_LENGTH_RANDOM_ID):
    """This function returns a random ID by using the uuid4 method. In order
    to have reasonably short IDs, the ID returned from uuid4() is truncated.
    This is not optimized for being collision-free. See documentation of uuid:
    http://docs.python.org/library/uuid.html
    http://en.wikipedia.org/wiki/Universally_unique_identifier
    """
    if length > MAX_LENGTH_RANDOM_ID:
        length = MAX_LENGTH_RANDOM_ID
    return str(uuid.uuid4())[0:length]

