import re
import toml
import sys
from more_itertools import split_before, grouper
from pathlib import Path

from tm_parser.config import Config
from tm_parser.utils import get_date


print(__file__, file=sys.stderr)

REQUIREMENTS = toml.load(Path(__file__).parent / "data" / "requirements.toml")

REVERSED_REQUIREMENTS = {}

for rank, data in REQUIREMENTS.items():
    if rank not in ["Star", "Life", "Eagle"]:
        continue
    for code, requirement in data["requirements"].items():
        if "troopmaster_name" in requirement.keys():
            REVERSED_REQUIREMENTS[(rank, requirement["troopmaster_name"])] = code


def rank_markers_test(line):
    """returns True if the line starts a new rank in the rank advancement
    Star, Life and Eagle are special because TM includes the # of merit badges
    and the requirement "Eagle Project", and the merit badge "Lifesaving" mess
    it up"""
    return (
        line in Config.RANKS
        or line.startswith("Eagle")
        and not line.startswith("Eagle MB")
        and not line.startswith("Eagle Project")
        or line.startswith("Star")
        or line.startswith("Life")
        and not line.startswith("Lifesaving")
    )


def parse_code(text, rank=None):
    if not isinstance(text, str):
        text = str(text)
    # one or two digits, then a lowercase letter (optional), then a period
    pat = re.compile(r"(\d{1,2})(\.?)([a-z]?)\.?")
    m = pat.match(text)
    if m:
        if len(m.group(1)) == 1:
            # single digit number
            return f"0{m.group(1)}{m.group(3)}"
        else:
            return m.group(1) + m.group(3)
    elif rank in ["Star", "Life", "Eagle"]:
        return get_upper_rank_code(rank, text)
    elif "Palm" in rank:
        return text


def get_upper_rank_code(rank, text):
    print(rank, text, file=sys.stderr)
    if (rank, text) not in REVERSED_REQUIREMENTS:
        return text
    print(REVERSED_REQUIREMENTS[(rank, text)], file=sys.stderr)
    return REVERSED_REQUIREMENTS[(rank, text)]


def get_rank_only(line):
    """returns the first rank that is included in the line"""
    for rank in Config.RANKS:
        if rank in line:
            return rank
    return None
    # return "".join(rank for rank in Config.RANKS if rank in line)


def get_rank_advancement(data):
    """take in data, split it on the rank header markers, and return a dictionary
    with the requirements as keys and the signoff-dates as values"""
    rank_data = list(split_before(data, rank_markers_test))

    # for each rank, make a dictionary where the keys are the requirements,
    # and the values are the date signed off

    output = {
        get_rank_only(rank[0]): {
            parse_code(requirement, rank=get_rank_only(rank[0])): get_date(date)
            for requirement, date in grouper(rank[1:], 2)
        }
        for rank in rank_data
    }
    return output
