from cs_parser import CsharpParser
from html import HtmlMaker
import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest="filename", help='path to the file you want to document')
    parser.add_argument('-s', '--show', help='show file contents', action='store_true')
    args = parser.parse_args()
    with open(args.filename, 'rt') as file:
        lines = file.readlines()
    parser = CsharpParser()
    oop_result = parser.parse_file(lines)
    name = args.filename.split(os.sep)[-1]
    maker = HtmlMaker()
    result = maker.make_html_file(oop_result, name[:-3])
    if args.show:
        print(f'File contents:\n{result}')

