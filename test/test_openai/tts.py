from pathlib import Path
from openai import OpenAI

client = OpenAI()
speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Today is a wonderful day to build something people love!",
)
#.with_streaming_response.with_streaming_response.method()
#response.stream_to_file(speech_file_path)
response.with_streaming_response(speech_file_path)
