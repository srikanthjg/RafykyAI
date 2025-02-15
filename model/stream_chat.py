#!/usr/bin/env python3

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Error: GEMINI_API_KEY environment variable not found!")
    exit(1)

genai.configure(api_key=API_KEY)


# Instantiate te model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
  system_instruction="You're a mediator in a multi-member online voice call. Your job is to be a keen listener and respond with helpful messages to facilitate the conversation flow. ",
)

# Start chat-session which will be continued 
chat_session = model.start_chat(
  history=[
    {
      "role": "model",
      "parts": [
        "You're Rafyky, a helpful assistant who joins online meetings and helps mediate the conversation.\n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Hey guys! Let's get started with our meeting.\n",
      ],
    },
  ]
)

print("\n### Rafyky - Streaming Mode (Type 'exit' or 'bye' to quit)\n")

# Continuous chat loop which includes streaming. 
while True:
    user_input = input("Human Speaker: ")
    if user_input.lower() in ['exit','bye','quit']:
        print("\n🔹 Exiting chat. Goodbye!\n")
        break

    try:
        response_stream = chat_session.send_message(user_input, stream=True)
        print("Rafyky: ", end="", flush=True)

        for chunk in response_stream:
            print(chunk.text, end="", flush=True)  # Streaming response
        print()  # Newline after full response

    except Exception as e:
        print("\n❌ Error:", str(e))