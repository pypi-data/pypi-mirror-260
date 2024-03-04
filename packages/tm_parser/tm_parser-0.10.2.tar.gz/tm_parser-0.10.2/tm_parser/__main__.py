"""
parser.py

from a troopmaster scout individual history report of all items, parse out
all kinds of scout information
"""

import click

from tm_parser import Parser


@click.command()
@click.option(
    "-t",
    "--output-type",
    default="yaml",
    help="output type, options are yaml (default), toml, and json",
)
@click.option("-o", "--outfile", help='output filename, default is "output')
@click.argument(
    "infile",
    type=click.File("rb"),
    default="data/tm_data.pdf",
)
def main(output_type=None, outfile=None, infile=None):
    """takes INFILE and outputs troopmaster data converted to standard out or to OUTFILE"""
    if not outfile:
        if not output_type:
            output_type = "json"
    elif outfile.endswith("json"):
        output_type = "json"
    elif outfile.endswith("yaml"):
        output_type = "yaml"
    elif outfile.endswith("toml"):
        output_type = "toml"
    parser = Parser(infile=infile, outfile=outfile, file_format=output_type)

    if outfile:
        parser.dump()
    else:
        print(parser.dumps())


if __name__ == "__main__":
    main()
