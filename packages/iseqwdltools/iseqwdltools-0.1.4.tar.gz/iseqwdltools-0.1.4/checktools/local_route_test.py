#!/usr/bin/env python3
import json
import argparse
import os.path
import git
import re
from packaging import version
import sys
import pathlib

__version__ = "0.0.1"


def args_parser_init() -> argparse.Namespace:
    """Get user inputs"""
    parser = argparse.ArgumentParser(
        description="""This script parses the input addresses in tests for the given test.json file and checks if any links to the local catalogues have been accidentally left in the code returning error when finding such.""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-j",
        "--test-jsons",
        type=str,
        nargs="+",
        required=True,
        help="",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s {}".format(__version__)
    )

    args = parser.parse_args()
    return args


class ExceptionThrower(Exception):
    def __init__(self, code, message):
        self.error_code = code
        self.message = message
        super().__init__(self.message)


restricted_paths = ["/home/"]
found_erroneous_paths = []


def main():
    args = args_parser_init()

    for file_path in args.test_jsons:
        with open(file_path) as user_file:
            json_data = json.loads(user_file.read())
            tests = json_data["tests"]
            for test in tests:
                input = test["inputs"]
                for key, value in input.items():
                    if any(value.startswith(path) for path in restricted_paths):
                        found_erroneous_paths.append(
                            f"Local address for the input file named: '{key}' found in inputs of file located at: {file_path}"
                        )

    if len(found_erroneous_paths):
        raise ExceptionThrower(422, "\n".join(found_erroneous_paths))


if __name__ == "__main__":
    main()
