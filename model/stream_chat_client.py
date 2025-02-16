import asyncio
import websockets

async def send_messages():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            message = input("Say something: ")
            await websocket.send(message)
            response = await websocket.recv()
            print(f"Rafyky responded: {response}")

if __name__ == "__main__":
    asyncio.run(send_messages())