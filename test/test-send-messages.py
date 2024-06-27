import asyncio
import websockets
import json
import random
from datetime import datetime


async def send_messages(uri, username):
    try:
        async with websockets.connect(uri) as websocket:
            print(f'{username} connected')

            # Simulate sending messages
            for _ in range(10):  # Each user sends 10 messages
                message = {
                    'content': f"Hello from {username} at {datetime.utcnow().isoformat()}",
                    'timestamp': datetime.utcnow().isoformat()
                }
                await websocket.send(json.dumps(message))
                print(f"{username} sent: {message['content']}")

                await asyncio.sleep(random.uniform(1, 3))  # Wait between 1 to 3 seconds

    except websockets.ConnectionClosed as e:
        print(f'Connection closed for {username}: {e}')
    except Exception as e:
        print(f'Error for {username}: {e}')


async def simulate_users(uri, num_users):
    users = [f"user_{i}" for i in range(num_users)]
    tasks = [send_messages(uri, username) for username in users]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    uri = "ws://localhost:8080/ws"
    num_users = 5  # Number of simulated users
    asyncio.run(simulate_users(uri, num_users))
