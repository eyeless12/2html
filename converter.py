from utils.cs_parser import CsharpParser
from utils.html import HtmlMaker
import argparse
import os


def main(filename, destination):
    with open(filename, 'rt') as file:
        lines = file.readlines()
    csparser = CsharpParser()
    oop_result = csparser.parse_file(lines)
    name = filename.split(os.sep)[-1]
    maker = HtmlMaker()
    result = maker.format_documentation(oop_result, name[:-3])
    if destination:
        path = f"{destination}"
    else:
        path = ""
    with open(f"{path + '/' if path else ''}{name[:-3]}.html", 'w') as f:
        f.write(result)
    print(f"Html document is at {path if path else 'code folder'}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest="filename", required=True)
    parser.add_argument('-d', dest="destination")
    args = parser.parse_args()
    main(args.filename, args.destination)
