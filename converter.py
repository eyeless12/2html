from utils.cs_parser import CsharpParser
from utils.html import HtmlMaker
import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest="filename", required=True)
    parser.add_argument('-d', dest="destination")
    args = parser.parse_args()
    with open(args.filename, 'rt') as file:
        lines = file.readlines()
    parser = CsharpParser()
    oop_result = parser.parse_file(lines)
    name = args.filename.split(os.sep)[-1]
    maker = HtmlMaker()
    result = maker.make_html_file(oop_result, name[:-3])
    if not args.destination:
        with open(f"{name[:-3]}.html", 'w') as f:
            f.write(result)
        print(f"File in code folder")
    else:
        if os.path.exists(args.destination):
            with open(f"{args.destination}/{name[:-3]}.html", 'w') as f:
                f.write(result)
            print(f"File at {args.destination}")