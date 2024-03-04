from itertools import chain

from more_itertools import pairwise

from .config import Config
from .utils import split_fields, split_pair, get_date


def get_oa_status(data):
    """split up the data, then make a dict with the field->value
    for each field. Necessary because Troopmaster exports
    fields with No data"""
    data = chain.from_iterable(split_fields(text) for text in data)
    output = {}
    for item1, item2 in pairwise(data):
        key, value = split_pair(item1, item2, lambda x: x in Config.OA_HEADERS)
        if key:
            output[key] = get_date(value)
    return output
