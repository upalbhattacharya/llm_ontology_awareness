#!/usr/bin/env python

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that classifies statements as  True or False only.",
        },
        {
            "role": "user",
            "content": "AlsaceRegion is a Wine",
        },
    ],
)

print(completion.choices[0].message.content)
