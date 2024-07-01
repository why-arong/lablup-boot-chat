import aiohttp
import aiohttp.web as web
import aiohttp_cors
import aiohttp_session
import aiohttp_session.redis_storage
from database import Database
import redis.asyncio as redis
import json
from datetime import datetime
import pytz
import bcrypt
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:abc@localhost/postgres')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
clients = []
db = Database(dsn=DATABASE_URL)

# Set the time zone to Asia/Seoul
tz = pytz.timezone('Asia/Seoul')

async def handle_websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    session = await aiohttp_session.get_session(request)
    username = session.get('username')

    if not username:
        await ws.send_str(json.dumps({'error': 'User not authenticated'}))
        await ws.close()
        return ws

    clients.append(ws)
    try:
        messages = await db.get_all_chats()
        for message in messages:
            # Convert timestamp to Asia/Seoul time zone
            local_timestamp = message['timestamp'].astimezone(tz).isoformat()
            await ws.send_str(json.dumps({
                'username': message['username'],
                'content': message['content'],
                'timestamp': local_timestamp,
            }))

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                content = data.get('content')
                timestamp = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(tz).isoformat()

                await db.save_chat(content, username)

                for client in clients:
                    if not client.closed:
                        await client.send_str(json.dumps({
                            'username': username,
                            'content': content,
                            'timestamp': timestamp
                        }))
                    else:
                        clients.remove(client)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print(f'WebSocket connection closed with exception {ws.exception()}')
    finally:
        clients.remove(ws)

    return ws

async def handle_signup(request):
    try:
        data = await request.json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return web.HTTPBadRequest(text='Missing username or password')

        await db.add_user(username, password)
        return web.Response(text=f'User {username} successfully signed up', status=200)
    except Exception as e:
        return web.HTTPInternalServerError(text=str(e))

async def handle_login(request):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return web.HTTPBadRequest()

    try:
        user = await db.get_user(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session = await aiohttp_session.new_session(request)
            session['username'] = username
            return web.json_response({'message': 'Login successful'})
        else:
            return web.HTTPUnauthorized(text='Invalid username or password')
    except Exception as e:
        return web.HTTPUnauthorized(text=str(e))

async def handle_session(request):
    session = await aiohttp_session.get_session(request)
    username = session.get('username')
    if username:
        return web.json_response({'username': username})
    else:
        return web.HTTPUnauthorized()

async def init_app():
    await db.init()
    app = web.Application()

    redis_client = redis.from_url(REDIS_URL)
    storage = aiohttp_session.redis_storage.RedisStorage(redis_client)
    aiohttp_session.setup(app, storage)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    app.router.add_get('/ws', handle_websocket)
    app.router.add_post('/signup', handle_signup)
    app.router.add_post('/login', handle_login)
    app.router.add_get('/session', handle_session)

    for route in list(app.router.routes()):
        cors.add(route)

    return app

if __name__ == '__main__':
    web.run_app(init_app(), host='0.0.0.0', port=8080)
