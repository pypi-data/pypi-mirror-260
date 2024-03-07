# SPDX-FileCopyrightText: 2023 Helge
# SPDX-FileCopyrightText: 2024 Helge
#
# SPDX-License-Identifier: MIT

import html
import json


def safe_first_element(item):
    """Returns the first element of a list, otherwise None"""
    if not item or not isinstance(item, list) or len(item) == 0:
        return None
    return item[0]


def escape_markdown(text):
    """Escapes markdown characters, necessary to display markdown (as done for firefish)"""

    text = text.replace("`", "\\`")
    text = text.replace("*", "\\*")
    text = text.replace("_", "\\_")
    text = text.replace("[", "\\[")
    text = text.replace("]", "\\]")
    return text


def pre_format(text):
    """Escapes html text to pre formatted markdown"""
    if text is None:
        return [""]
    if isinstance(text, bool):
        return ["true" if text else "false"]
    return ["".join(f"<pre>{html.escape(x)}</pre>" for x in text.split("\n"))]


def sanitize_backslash(x):
    return x.replace("|", "\\|")


def format_as_json(data, small=False):
    """Displays a dictionary as pretty printed json.

    :param small: If true sets font-size to 75%."""
    style = "line-height:1;"
    if small:
        style += "font-size:75%;"

    return [
        "".join(
            f"<pre style='{style}'>{sanitize_backslash(x)}</pre>"
            for x in json.dumps(data, indent=2).split("\n")
        )
    ]
