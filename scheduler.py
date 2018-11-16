#!/usr/bin/env python
import sys
from .schedule_parser import ScheduleParser

def run():
    json_file = None
    if len(sys.argv) >= 2:
        json_file = sys.argv[1]

    parser = ScheduleParser(json_file)
    parser.load_contents()
    parser.reorder()
    parser.print_class_order()

if __name__ == '__main__':
    run()
