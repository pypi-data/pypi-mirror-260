from datetime import datetime, date
import json
import yaml
import toml


class DateTimeEncoder(json.JSONEncoder):
    """allows json encoder to write datetime or date items as isoformat"""

    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


def dump_string(output, dump_type):
    """take the output and a file type
    and dump the output to a string"""
    match dump_type:
        case "json":
            return json.dumps(output, cls=DateTimeEncoder)
        case "yaml":
            return yaml.dump(output)
        case "toml":
            return toml.dumps(output)


def dump_file(output, dump_type, outfile=None):
    """take the output and a file type
    and dump the output to the appropriate filetype as a string
    if you want it dumped to an output file, pass a file handle as outfile
    """
    match dump_type:
        case "json":
            json.dump(output, outfile, cls=DateTimeEncoder)
        case "yaml":
            yaml.dump(output, outfile)
        case "toml":
            toml.dump(output, outfile)
