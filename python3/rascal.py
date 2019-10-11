#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================================
# Rascal - String manipulation tool
# Character replacement script
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# Website: http://www.urbanware.org
# GitHub: https://github.com/urbanware-org/rascal
# ============================================================================

import os
import sys

def main():
    from core import clap
    from core import replace as r

    try:
        p = clap.Parser()
    except Exception as e:
        print("%s: error: %s" % (os.path.basename(sys.argv[0]), e))
        sys.exit(1)

    p.set_description("Replace characters in a string with a random one " \
                      "from a user-defined character list.")
    p.set_epilog("Further information and usage examples can be found " \
                 "inside the documentation file for this script.")

    # Define required arguments
    p.add_avalue("-c", "--config-file", "config file path", "config_file",
                 None, True)
    p.add_avalue("-s", "--string", "input string to modify", "string", None,
                 True)

    # Define optional arguments
    p.add_switch("-h", "--help", "print this help message and exit", None,
                 True, False)
    p.add_switch("-l", "--length", "sort output strings by their length",
                 "length", True, False)
    p.add_avalue("-n", "--number", "number of strings to return", "number", 1,
                 False)
    p.add_switch("-m", "--remove-chars", "remove certain user-defined " \
                 "characters from input string", "remove_chars", True,
                 False)
    p.add_switch("-r", "--remove-spaces", "remove all spaces from input " \
                 "string", "remove_spaces", True, False)
    p.add_switch(None, "--version", "print the version number and exit", None,
                 True, False)

    if len(sys.argv) == 1:
        p.error("At least one required argument is missing.")
    elif ("-h" in sys.argv) or ("--help" in sys.argv):
        p.print_help()
        sys.exit(0)
    elif "--version" in sys.argv:
        print(r.get_version())
        sys.exit(0)

    args = p.parse_args()
    try:
        output = r.replace_chars(args.config_file, args.string,
                                 args.remove_spaces, args.remove_chars,
                                 args.number, args.length)
        for string in output:
            print(string)
    except Exception as e:
        p.error(e)

if __name__ == "__main__":
    main()

# EOF

