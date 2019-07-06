#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

# Dictionary containing the regular expressions.
re_dict = {
    'first_name': r'First\s+name:\s(([a-zA-Z-.]+)?(\s+)?([a-zA-Z-.]+)?(\s+)?([a-zA-Z-.]+)?)\n',
    'middle_name': r'Middle\s+name\(s\):\s(([a-zA-Z-.]+)?(\s+)?([a-zA-Z-.]+)?(\s+)?([a-zA-Z-.]+)?)\n',
    'surname': r'Surname:\s(([a-zA-Z-.]+)?(\s+)?([a-zA-Z-.]+)?(\s+)?([a-zA-Z-.]+)?)\n',
    'citizenship': r'Country of citizenship \(if known\):\s(([a-zA-Z-.]+)?(\s+)?([a-zA-Z-.]+)?(\s+)?([a-zA-Z-.]+)?)',
    'entity_name': r'Entity name:\s(([a-zA-Z0-9-.]+)?(\s+)?([a-zA-Z0-9-.]+)?(\s+)?([a-zA-Z0-9-.]+)?(\s+)?([a-zA-Z0-9-.]+)?(\s+)?([a-zA-Z0-9-.]+)?)\n',
    'entity_aff': r'Country of affiliation, ownership or registration:\s(([a-zA-Z-.]+)?(\s+)?([a-zA-Z-.]+)?(\s+)?([a-zA-Z-.]+)?(\s+)?([a-zA-Z-.]+)?(\s+)?([a-zA-Z-.]+)?(\s+)?([a-zA-Z-.]+)?(\s+)?([a-zA-Z-.]+)?)',
    'name_screen': r'Name to be screened\s?-\s?(Person|Entity)',
    'search_type': r'required:\s?(Precise|Near)',
    'dob': r'Date of birth \(if known\):\s(\d+|\w+)?(/|-|\.)(\d+|\w+)?(/|-|\.)(\d+|\w+)?',
}


def re_match(user_form, re_input):
    """Outputs a .group(1) string from a regular expression match."""
    re_match = re.compile(re_input)
    re_match = re_match.search(user_form)
    if re_match:
        return re_match.group(1).strip()


def re_match_dob(user_form, re_input):
    """
    Outputs a tuple containing .group(1), group(3), and group(5) strings 
    from a regular expression match.
    """
    re_match = re.compile(re_input)
    re_match = re_match.search(user_form)
    if re_match:
        return (re_match.group(1).strip(), re_match.group(3).strip(),
                re_match.group(5).strip())
