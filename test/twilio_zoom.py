#!/usr/bin/env python3
"""
A simple script that makes your Twilio number call a Zoom dial‐in number,
and automatically sends the meeting ID (and passcode, if provided) via DTMF.
"""

import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Dial

# Load credentials and numbers from environment variables
account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_TOKEN")
twilio_number = input("")          # e.g., "+1234567890"


zoom_dial_in_number = input("Enter zoom dial-in number:") # e.g., "+19876543210"
zoom_meeting_id = input("Enter zoom meeting id:")          # e.g., "1234567890"
zoom_passcode = input("Enter zoom pass code:")          # Optional

# Construct the DTMF sequence:
# Use "w" to wait (each "w" is a short pause) then the meeting ID, then "#" to indicate end.
# If a passcode is needed, append it (followed by "#").
send_digits = f"ww{zoom_meeting_id}#"
if zoom_passcode:
    send_digits += f"{zoom_passcode}#"

# Create a TwiML response that dials the Zoom dial‐in number and sends DTMF digits.
response = VoiceResponse()
dial = Dial()
# The 'sendDigits' attribute sends the DTMF sequence after the call connects.
dial.number(zoom_dial_in_number, sendDigits=send_digits)
response.append(dial)

# Initialize Twilio REST API client
client = Client(account_sid, auth_token)

# Place the call using the inline TwiML instructions.
call = client.calls.create(
    # to=zoom_dial_in_number,
    to=zoom_dial_in_number,
    from_=twilio_number,
    twiml=response.to_xml()
)

print(f"Call initiated with SID: {call.sid}")
