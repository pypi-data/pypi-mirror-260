from itertools import chain
from more_itertools import pairwise

from .config import Config

from .utils import split_fields, split_pair


def get_activity_totals(data):
    """go through the activity totals and make a dict.
    the hiking miles and service hours can be non-integer
    camping nights are always an integer"""
    data = chain.from_iterable(split_fields(text) for text in data)
    output = {}
    for item1, item2 in pairwise(data):
        key, value = split_pair(item1, item2, lambda x: x in Config.ACTIVITY_HEADERS)
        if key == "Miles Hiking":
            output["Miles Hiking"] = float(value)
        if key == "Service Hours":
            output["Service Hours"] = float(value)
        if key == "Total Nights Camping":
            output["Camping Nights"] = int(value)
    return output
