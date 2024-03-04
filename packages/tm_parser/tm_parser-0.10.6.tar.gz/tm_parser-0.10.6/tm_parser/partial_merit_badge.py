from itertools import chain
import re

from more_itertools import pairwise

from .config import Config

from .utils import split_fields, split_pair


def parse_partial_mb_name(line):
    pat = re.compile(r"(.*?)(\*)? ?\((\d*)?\)")
    m = re.match(pat, line.strip(":"))
    if m:
        return m.group(1), {
            "eagle_required": bool(m.group(2)),
            "version": m.group(3),
        }
    return None


def partial_fields_test(line):
    """returns True if a line starts with a partial merit badge header or is a partial MB name"""
    return any(line.startswith(marker) for marker in Config.PARTIAL_MB_HEADERS) or bool(
        parse_partial_mb_name(line)
    )


def get_partials(data):
    data = chain.from_iterable(split_fields(text) for text in data)
    output = {}
    for item1, item2 in pairwise(data):
        if item1 and item2:
            k, v = split_pair(item1, item2, partial_fields_test)
            # print(f"k = '{k}', v = '{v}'")
            if k and parse_partial_mb_name(k):
                name, mb_data = parse_partial_mb_name(k)
                output[name] = mb_data
                output[name]["Open Reqts"] = []
            elif k == "Open Reqts":
                #    print(f"got some requirements {v}")
                if v and v.startswith("Error"):
                    continue
                if v:
                    for item in re.split(", *", v):
                        #            print(f"adding requirement {item}")
                        output[name][k].extend(parse_partial_req(item))
            elif item1[0].isdigit() and item2[0].isdigit():
                #    print(f"adding requirements from {item1}, {item2}")
                if item2:
                    #        print(item2)
                    for item in re.split(", *", item2):
                        #            print(item)
                        output[name]["Open Reqts"].extend(parse_partial_req(item))
            elif k:
                output[name][k] = v
    return output


def parse_partial_req(item):
    if not item:
        return []

    if output := partial_class_1(item):
        return output
    if output := partial_class_2(item):
        return output
    if output := partial_class_3(item):
        return output
    if output := partial_class_4(item):
        return output
    if output := partial_class_5(item):
        return output


def partial_class_1(item):
    """checks if the item contains just a bunch of digits"""
    if all(i.isdigit() for i in item):
        return item
    return None


def partial_class_2(item):
    """checks if the item has digits and then small letters,
    a dot and then several numbers"""
    output = []
    pat = re.compile(
        r"""
                     (?P<requirement>\d+)  # start with any number of digits
                        (?P<sub>[a-z]+)        # any number of lowercase letters
                     \.?                # optional dot
                     (?P<subsub>\d+)?             # any number of digits (optional)
                      """,
        re.X,
    )
    m = re.match(pat, item)
    if m:
        if m.group("sub"):
            for sub in m.group("sub"):
                if m.group("subsub"):
                    for subsub in m.group("subsub"):
                        output.append("".join((m.group("requirement"), sub, subsub)))
                else:
                    output.append("".join((m.group("requirement"), sub)))
        return output


def partial_class_3(item):
    """checks if the partial requirement is
    a number, then a capital letter, a dot
    and small letter with numbers"""
    output = []
    pat = re.compile(
        r"""(?P<requirement>\d+)
                      (?P<subcap>[A-Z])\.?
                      (?P<subcapsubs>([a-z]\d?)+)+""",
        re.X,
    )
    m = re.match(pat, item)
    if m:
        if m.group("subcap"):
            for subcap in m.group("subcap"):
                if m.group("subcapsubs"):
                    for subcapsubs in re.findall(r"[a-z]\d?", m.group("subcapsubs")):
                        output.append(
                            "".join((m.group("requirement"), subcap, subcapsubs))
                        )
                else:
                    output.append("".join((m.group("requirement"), subcap)))

        return output


def partial_class_4(item):
    """checks whether the item is digits, then a dot, then more digits"""
    output = []
    pat = re.compile(r"""(?P<requirement>\d+)\.(?P<digit>\d+)""")
    m = re.match(pat, item)
    if m:
        for digit in m.group("digit"):
            output.append("".join((m.group("requirement"), ".", digit)))
        return output


def partial_class_5(item):
    """checks whether the item is digits, then a capital letter then
    numerals and letters like this 5A.1a1b1cde"""
    output = []
    pat = re.compile(
        r"""(?P<requirement>\d+)
                      (?P<subcap>[A-Z])\.
                      (?P<subcapsubs>(\d[a-z]?)+)+""",
        re.X,
    )
    m = re.match(pat, item)
    if m:
        if m.group("subcap"):
            for subcap in m.group("subcap"):
                if m.group("subcapsubs"):
                    for subcapsubs in re.findall(r"\d[a-z]?", m.group("subcapsubs")):
                        output.append(
                            "".join((m.group("requirement"), subcap, subcapsubs))
                        )
                else:
                    output.append("".join((m.group("requirement"), subcap)))

        return output
