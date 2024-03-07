# SPDX-FileCopyrightText: 2023 Helge
# SPDX-FileCopyrightText: 2024 Helge
#
# SPDX-License-Identifier: MIT

from .types import InputData

examples = [
    {"content": "Link", "attachment": {"href": "https://funfedi.dev", "type": "Link"}},
    {
        "content": "Payment Link, see FEP-0ea0",
        "attachment": {
            "type": "Link",
            "name": "Donate",
            "href": "payto://iban/DE75512108001245126199",
            "rel": "payment",
        },
    },
    {
        "content": "Text document",
        "attachment": {
            "type": "Document",
            "name": "text document",
            "href": "http://pasture_one_actor/assets/sample.txt",
        },
    },
    {
        "content": "attached note",
        "attachment": {
            "type": "Note",
            "attributedTo": "http://pasture_one_actor/actor",
            "name": "attached note",
            "content": "This is just a note",
            "published": "2024-03-06T07:23:56Z",
        },
    },
    {
        "content": "Recipe",
        "attachment": {
            "@context": "https://schema.org/docs/jsonldcontext.jsonld",
            "@type": "Recipe",
            "name": "Peanut Butter and Jelly Sandwich",
            "recipeIngredient": [
                "Bread",
                "Peanut Butter",
                "Raspberry Jam",
                "Coffee (optional)",
            ],
            "recipeCategory": "Breakfast",
            "recipeInstructions": [
                {
                    "@type": "HowToStep",
                    "text": "Take a slice of bread and put it on a plate",
                },
                {"@type": "HowToStep", "text": "Spread peanut butter on the bread"},
                {
                    "@type": "HowToStep",
                    "text": "Spread raspberry jam on top of the peanut butter",
                },
                {
                    "@type": "HowToStep",
                    "text": "Eat your PB&J Sandwich and drink your coffee if you have it",
                },
                {
                    "@type": "HowToStep",
                    "text": "Check if you are still hungry, if yes a repeat step 1",
                },
            ],
        },
    },
    {
        "content": "10 images",
        "attachment": [
            {
                "type": "Document",
                "url": f"http://pasture_one_actor/images/10{x}.png",
            }
            for x in range(1, 11)
        ],
    },
]


data = InputData(
    title="Attachments",
    frontmatter="""
""",
    filename="attachments.md",
    examples=examples,
    detail_table=False,
    support_table=False,
)
