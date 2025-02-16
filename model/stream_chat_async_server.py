#!/usr/bin/env python3

import os
import uvicorn
from fastapi import FastAPI, WebSocket

import google.generativeai as genai
from dotenv import load_dotenv

from datetime import datetime


# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise EnvironmentError("GEMINI_API_KEY environment variable not found!")

class StreamChat:
    def __init__(self, api_key: str, persona: str):
        # Configure the generative AI library with your API key.
        genai.configure(api_key=api_key)

        self.persona = persona

        # Set up the generation configuration.
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        # Instantiate the model with a system instruction.
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=self.generation_config,
            system_instruction=(
                f"You're an AI assistant who joins as a member in a multi-member online voice call. "
                f"Your role is to exactly be the persona assigned to you as follows. "
                f"{persona}"
            ),
        )


        # Start a chat session with some initial history.
        self.chat_session = self.model.start_chat(
            history=[
                # {
                #     "role": "model",
                #     "parts": [
                #         "I'm Rafyky, a helpful assistant and I can help mediate the conversation.\n"
                #     ],
                # },
                {
                    "role": "user",
                    "parts": [
                        "Hey guys! Let's get started with our meeting.\n"
                    ],
                },
            ]
        )

        print(f"\n### Rafyky Server started. \n\n## Persona: [[{self.persona}]]\n\n##Listening ... \n")

    def send_message(self, message: str, stream: bool = False):
        """Send a message to the chat session."""
        return self.chat_session.send_message(message, stream=stream)

def create_app(persona: str) -> FastAPI:
    """Create and configure the FastAPI app."""
    app = FastAPI()

    # Instantiate the StreamChat with the API key.
    stream_chat = StreamChat(API_KEY, persona)

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        while True:
            try:
                # Receive message from client.
                data = await websocket.receive_text()
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Received message: {data}")


                # Send the message and stream the response.
                response_text = ""
                response_stream = stream_chat.send_message(data, stream=True)
                for chunk in response_stream:
                    print(chunk.text, end="", flush=True)
                    response_text += chunk.text

                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Response message:{response_text}\n---------\n")
                # Send the complete response back to the client.
                await websocket.send_text(response_text)
            except Exception as e:
                print(f"Connection closed or error occurred: {e}")
                break

    return app

# Create the FastAPI app instance.

trump_persona = "Annoying guy who talks about politics after everything. He cannot stop saying that Trump is a great guy and brings him into every conversation"
thoughtful_listener_persona = "A very silent guy who stays absolutely quiet unless someone uses angry or hateful language. In that case, politely ask them not to and encourage them to have a meaningful conversation"

app = create_app(persona=trump_persona)

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)