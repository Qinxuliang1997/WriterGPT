# from django.test import TestCase

import os
from openai import OpenAI
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_API_KEY"),
)
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test, give me some faith",
        }
    ],
    model="gpt-3.5-turbo-1106",
)
print(chat_completion.choices[0].message.content)