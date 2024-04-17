# from django.test import TestCase

import os
from openai import OpenAI
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key='',
)
print(os.environ.get("OPENAI_API_KEY"))
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "请你给出下面这篇文章的提纲.\n keyword: 五代第一明君——柴荣",
        }
    ],
    model="gpt-3.5-turbo",
)
print(chat_completion.choices[0].message.content)