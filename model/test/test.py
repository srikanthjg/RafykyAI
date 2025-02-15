import json
import time

import sys
import os

# Get the parent directory of 'test/'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#from stream_chat import model 

# Load the conversation JSON file
with open("conversation.json", "r") as file:
    data = json.load(file)

# Replay the conversation with pauses
for entry in data["conversation"]:
    time.sleep(entry["time"]/2)  # Simulating the pauses in conversation
    print(f'{entry["speaker"]}: {entry["text"]}')
    #model.send_message("hello")
    #break

