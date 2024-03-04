from itertools import chain

from more_itertools import (
    pairwise,
)

from .utils import get_date

from .config import Config

from .utils import (
    split_fields,
    split_pair,
)

def get_scout_data(data):
    """take in an iterable of rows of data, process them into a dict
    with key-> value pairs
    """
    data = chain.from_iterable(split_fields(text) for text in data)
    output = {}

    for item1, item2 in pairwise(data):
        # if key is a valid key for scout data, you'll get either
        # if item1 and item2 are valid keys -> item1, None
        # if item1 is a key and item2 is a value -> item1, value
        key, value = split_pair(
            item1, item2, lambda x: x in (*Config.TEXT_FIELDS, *Config.DATE_FIELDS)
        )
        if key in Config.DATE_FIELDS:
            # get_date returns either a datetime object or None"""
            output[key] = get_date(value)
            if key == "Date":
                output["Rank Date"] = output[key]
                del output[key]
        elif key:
            output[key] = value
    return output


def find_scout_name(scout_info):
    """take a list of strings and find the scout name field"""
    for field, data in pairwise(scout_info):
        if field.startswith("Name:"):
            return data
    return None
