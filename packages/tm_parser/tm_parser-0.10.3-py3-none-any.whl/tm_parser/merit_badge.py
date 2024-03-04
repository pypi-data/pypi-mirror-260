from itertools import chain

from more_itertools import chunked

from .utils import get_date, parse_merit_badge


def split_badge(item):
    """some merit badges are too long like "Emergency Preparedness* 06/20/22"
    fortunately these are all longer than 22 characters, so we split them at the *"""
    if len(item) > 23:
        output = list(item.rsplit(" ", 1))
        return output
    return [item]


def get_full_merit_badges(lines):
    """take a stream of merit badge lines from a pdf"""
    output = chain.from_iterable([split_badge(m) for m in lines])
    data = {}
    for item, date_str in chunked(output, 2):
        date = get_date(date_str)
        badge = parse_merit_badge(item)
        data[badge["name"]] = {
            "eagle_required": badge["eagle_required"],
            "date": date,
        }
    return data
