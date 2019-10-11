#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ============================================================================
# Rascal - String manipulation tool
# Character replacement core module
# Copyright (C) 2019 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/rascal
# GitLab: https://gitlab.com/urbanware-org/rascal
# ============================================================================

__version__ = "1.0.4"

import ConfigParser
import os
import paval as pv
import random
import sys


def get_version():
    """
        Return the version of this module.
    """
    return __version__


def replace_chars(config_file, string="", remove_spaces=False,
                  remove_chars=False, number=1, sort_length=False):
    """
        Replace characters in a string based on the given config file.
    """
    pv.string(string, "string to modify")
    pv.intrange(number, "number of strings", 1, None)
    try:
        pv.path(config_file, "config", True, True)
    except:
        config_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        config_file = \
            os.path.join(config_dir, "cfg", os.path.basename(config_file))
        pv.path(config_file, "config", True, True)

    config_file = os.path.abspath(config_file)
    number = int(number)

    if remove_spaces:
        string = string.replace(" ", "")

    if remove_chars:
        chars = __read_option(config_file, "Remove", "Characters")
        chars = chars.replace(" ", "")

        for char in chars:
            string = string.replace(char, "")

    dict_chars = {}
    for char in string:
        if char in ("[", "]", "=", ";", ","):
            continue

        value = __read_option(config_file, "Replace", char.upper())
        if char not in dict_chars:
            replace_chars = value.strip(", ").replace(" ", "").split(",")
            dict_chars.update({char: replace_chars})

    output = []
    for n in range(number):
        string_new = __transform(string, output, dict_chars)
        output.append(string_new)

    if sort_length:
        output = sorted(output, key=len, reverse=True)

    return output


def __transform(string, string_list, dict_chars):
    """
        Core method to scramble the given string based on the given config
        file.
    """
    string_new = ""
    for char in string:
        replace_chars = dict_chars.get(char)
        if replace_chars is None or replace_chars[0] == "":
            string_new += char
            continue

        random.seed()
        rnd = random.randint(0, len(replace_chars) - 1)
        string_new += replace_chars[rnd]

    while string_new is None or string_new in string_list:
        try:
            string_new = __transform(string, string_list, dict_chars)
        except:
            raise Exception("The input string seems to be too short to "
                            "return the requested amount of data.")

    return string_new


def __read_option(file_path, section, option):
    """
        Method to parse the config file and read out its values.
    """
    c = ConfigParser.RawConfigParser()
    c.read(file_path)

    value = ""
    try:
        value = c.get(section, option)
    except ConfigParser.NoSectionError:
        value = ""
    except ConfigParser.NoOptionError:
        value = ""

    return str(value)

# EOF
