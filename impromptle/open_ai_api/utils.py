from openai import OpenAI
from django.conf import settings

# Instantiate the OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

print("Using OpenAI API Key:", settings.OPENAI_API_KEY)


def ask_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Adjust model as needed
        messages=[{"role": "user", "content": prompt}],
    )

    # The new response objects are now pydantic models
    return response.choices[0].message['content'].strip()
