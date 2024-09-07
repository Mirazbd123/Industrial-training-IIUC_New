import os
from dotenv import load_dotenv

from groq import Groq
load_dotenv()
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def summarize(text):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"summarize the text in bangla {text}",
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content