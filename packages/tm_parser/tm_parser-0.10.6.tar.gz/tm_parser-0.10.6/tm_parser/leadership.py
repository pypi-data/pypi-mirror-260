from .utils import get_date


def get_leadership_dates(line):
    """takes in "date - date #" and splits it into two dates and
    whether it counts for rank advancement (denoted by not having
    a hash symbol"""
    item1, item2 = line.split(" - ")
    item2, *rank_no_counts = item2.split()
    return {
        "start": get_date(item1),
        "end": get_date(item2),
        "for_rank": not rank_no_counts,
    }
