import openai

# Call the TTS‑1 endpoint (this is a hypothetical API call)
response = openai.Audio.create(
    model="tts-1",
    text="Hello, world! This is a test of the TTS system.",
    voice="en-US"  # (Optional) Specify a voice if supported
)

# Save the returned audio data to a file
with open("output.wav", "wb") as audio_file:
    audio_file.write(response["audio_data"])

print("Audio has been saved to output.wav")
