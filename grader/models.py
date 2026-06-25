import os
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
model_mistral = "mistral-large-latest"

client_mistral = Mistral(api_key=api_key)

def call_mistral(input,temperature=0.6):
    chat_response = client_mistral.chat.complete(
    model= model_mistral,
    messages = [
        {
            "role": "user",
            "content": input,
        },
        
    ],
    temperature=temperature
    )
    return chat_response.choices[0].message.content
