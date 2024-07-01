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
        'Cookie': f'AIOHTTP_SESSION={session_cookie}'  # Correctly format the session cookie header
    }
    ws_uri = uri.replace('http', 'ws') + '/ws'
    try:
        async with websockets.connect(ws_uri, extra_headers=headers) as websocket:
            print(f'{username} connected')

            # Simulate sending messages
            for _ in range(10):  # Each user sends 10 messages
                message = {
                    'content': f"Hello from {username} at {datetime.utcnow().isoformat()}",
                    'timestamp': datetime.utcnow().isoformat()
                }
                await websocket.send(json.dumps(message))
                print(f"{username} sent: {message['content']}")

                await asyncio.sleep(random.uniform(1, 3))

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

            # Sign up the user
            await signup_user(session, uri, username, password)

            # Log in the user
            session_cookie = await login_user(session, uri, username, password)
            print(session_cookie)
            if session_cookie:
                tasks.append(send_messages(uri, username, session_cookie))

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    uri = "http://localhost:8080"
    num_users = 3  # Number of simulated users
    user_data = [
        {'username': 'mangul2', 'password': 'gom2'},
        {'username': 'ming2', 'password': 'k2'},
        {'username': 'pil2', 'password': 'mo2'}
    ]
    asyncio.run(simulate_users(uri, num_users, user_data))
