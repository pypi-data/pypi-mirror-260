from datetime import datetime
import re

from .config import Config


def split_fields(text):
    """take a line that contains a colon and split into
    two parts if there's something before and after"""
    return (item.strip() for item in re.split(":", text) if item)


def split_pair(item1, item2, is_field):
    """takes two items and a callable is_field function

    used to take pairs of items and figure out if we should insert a None in between them.
    """
    return (
        item1 if is_field(item1) else None,
        item2 if is_field(item1) and not is_field(item2) else None,
    )


def section_markers_test(line):
    """figures out if our current line is a section divider"""
    return line in Config.SECTION_MARKERS or line.startswith("Merit Badges : ")


def get_date(text):
    try:
        if not text or "_" in text:
            return None
        elif "/" in text:
            return datetime.strptime(text, "%m/%d/%y").date() if text else None
        elif "-" in text:
            return datetime.strptime(text, "%Y-%m-%d").date() if text else None
    except ValueError:
        return text


def parse_merit_badge(text):
    pat = re.compile(
        r"""^(.*?)          # merit badge name
                          (\ \((.*)\))?  # optional space and version name
                          (\*)?$         # optional * to denote eagle required
                      """,
        re.X,
    )
    m = pat.match(text)
    if m:
        return {
            "name": m.group(1),
            "version": m.group(3) or None,
            "eagle_required": bool(m.group(4)),
        }
    else:
        return {
            "name": text,
            "version": None,
            "eagle_required": False,
        }
