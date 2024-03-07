# SPDX-FileCopyrightText: 2023 Helge
# SPDX-FileCopyrightText: 2024 Helge
#
# SPDX-License-Identifier: MIT

from .types import InputData

in_reply_to_examples = [
    {
        "content": "valid uri",
        "inReplyTo": "http://pasture_one_actor/assets/note1.jsonap",
    },
    {"content": "invalid uri", "inReplyTo": "http://invalid.example/"},
    {"content": "list", "inReplyTo": ["http://pasture_one_actor/assets/note1.jsonap"]},
    {
        "content": "Link in inReplyTo",
        "inReplyTo": {
            "type": "Link",
            "href": "http://pasture_one_actor/assets/note1.jsonap",
        },
    },
    {
        "content": "two elements in inReplyTo",
        "inReplyTo": [
            "http://pasture_one_actor/assets/note1.jsonap",
            "http://pasture_one_actor/assets/note2.jsonap",
        ],
    },
    {
        "content": "collection",
        "inReplyTo": {
            "type": "Collection",
            "items": ["http://pasture_one_actor/actor"],
        },
    },
    {
        "content": "embedded note",
        "inReplyTo": {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Note",
            "id": "http://pasture_one_actor/assets/note1.jsonap",
            "to": ["as:Public"],
            "attributedTo": "http://pasture_one_actor/actor",
            "content": "One",
            "published": "2024-01-06T13:11:45Z",
        },
    },
]


data = InputData(
    title="inReplyTo",
    frontmatter="""
The property is defined [here](https://www.w3.org/TR/activitystreams-vocabulary/#dfn-inreplyto). The
goal of this support table is to show how applications react to `inReplyTo` containing a wide variation
of allowed objects. As Fediverse applications generally only give one the option to reply to a single
element, the lacking support should not be surprising.
""",
    filename="in_reply_to.md",
    examples=in_reply_to_examples,
    detail_table=False,
    support_table=True,
    support_title="",
    support_result={
        "activity": lambda x: x["object"]["content"],
        "mastodon": lambda x: "✅" if x else "❌",
        "firefish": lambda x: "✅" if x else "❌",
    },
)
