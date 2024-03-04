from .pdf import parse_file
from .output import dump_string, dump_file
from .config import Config


class Parser:
    def __init__(self, infile=None, config=Config, outfile=None, file_format=None):
        self.config = Config
        if infile:
            self.input_file = infile
        if outfile:
            self.output_file = outfile
        if file_format:
            self.output_format = file_format
        else:
            self.output_format = "yaml"
        self.raw_scouts = []
        self.scouts = parse_file(self.input_file)

    def __len__(self):
        return len(self.scouts)

    def __iter__(self):
        for scout, data in self.scouts.items():
            yield scout, data

    def __str__(self):
        if not self.scouts:
            raise ValueError("No scout data found, run parse() first")
        return dump_string(self.scouts, self.output_format)

    def dump(self, outfile=None, file_format=None):
        if outfile:
            file = outfile
        elif self.output_file:
            file = self.output_file
        else:
            raise ValueError("no output file specified")

        if file_format:
            filetype = file_format
        elif self.output_format:
            filetype = file_format
        elif file.split(".")[-1].lower() in ("yaml", "toml", "json"):
            filetype = file.split(".")[-1].lower()
        else:
            raise ValueError("no output format specified")

        if not self.scouts:
            raise ValueError("No scout data found, run parse() first")
        with open(file, "w", encoding="utf-8") as f:
            dump_file(self.scouts, filetype, outfile=f)

    def dumps(self, format=None):
        if format in ("json", "yaml", "toml"):
            text_format = format
        else:
            text_format = self.output_format

        if not self.scouts:
            raise ValueError("No scout data found, run parse() first")
        return dump_string(self.scouts, text_format)
