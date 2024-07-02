import asyncio
import aiohttp
import websockets
import json
import random
from datetime import datetime

async def signup_user(session, uri, username, password):
    async with session.post(f'{uri}/signup', json={'username': username, 'password': password}) as response:
        if response.status == 200:
            print(f'Signup successful for {username}')
        else:
            print(f'Signup failed for {username}: {await response.text()}')

async def login_user(session, uri, username, password):
    async with session.post(f'{uri}/login', json={'username': username, 'password': password}) as response:
        if response.status == 200:
            print(f'Login successful for {username}')
            cookies = session.cookie_jar.filter_cookies(uri)
            return cookies['AIOHTTP_SESSION'].value  # Assuming the session cookie name is 'AIOHTTP_SESSION'
        else:
            print(f'Login failed for {username}: {await response.text()}')
            return None

async def send_messages(uri, username, session_cookie):
    headers = {
        'Cookie': f'AIOHTTP_SESSION={session_cookie}'
    }
    ws_uri = uri.replace('http', 'ws') + '/ws'
    try:
        async with websockets.connect(ws_uri, extra_headers=headers) as websocket:
            print(f'{username} connected')

            for _ in range(10):  # Each user sends 10 messages
                message = {
                    'content': f"Hello from {username} at {datetime.utcnow().isoformat()}",
                    'timestamp': datetime.utcnow().isoformat()
                }
                await websocket.send(json.dumps(message))
                print(f"{username} sent: {message['content']}")

                # No delay

    except websockets.ConnectionClosed as e:
        print(f'Connection closed for {username}: {e}')
    except Exception as e:
        print(f'Error for {username}: {e}')
    finally:
        if websocket.open:
            await websocket.close()
        print(f'{username} WebSocket closed properly')

async def simulate_users(uri, num_users, user_data):
    async with aiohttp.ClientSession() as session:
        tasks = []

        for user in user_data:
            username = user['username']
            password = user['password']

            await signup_user(session, uri, username, password)
            session_cookie = await login_user(session, uri, username, password)
            if session_cookie:
                tasks.append(send_messages(uri, username, session_cookie))

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    uri = "http://localhost:8080"
    num_users = 10  # Number of simulated users
    user_data = [
        {'username': f'user{i}', 'password': f'password{i}'} for i in range(num_users)
    ]
    asyncio.run(simulate_users(uri, num_users, user_data))
