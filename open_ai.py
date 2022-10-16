import openai
import os
import sys

OAI_API_KEY = os.environ.get('OAI_API_KEY')

if not OAI_API_KEY:
    print('ERROR: Open AI API key not set')
    sys.exit(1)


openai.api_key = OAI_API_KEY


def ai_completion(prompt):
    
    # Define specifications per documentation
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0,
        max_tokens=100,
    )
    # Return computer answer as str
    return response["choices"][0]["text"]