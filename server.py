import aiohttp
import aiohttp.web as web
import aiohttp_cors
import aiohttp_session
import aiohttp_session.redis_storage
from database import Database
import redis.asyncio as redis
import json
from datetime import datetime

clients = []
db = Database(dsn='postgresql://postgres:abc@localhost/postgres')

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
    # Send existing messages to the newly connected client
    messages = await db.get_all_chats()
    for message in messages:
        await ws.send_str(json.dumps({
            'username': message['username'],
            'content': message['content'],
            'timestamp': message['timestamp'].isoformat(),
        }))

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            data = json.loads(msg.data)
            content = data.get('content')
            timestamp = datetime.utcnow().isoformat()

            await db.save_chat(content, username)

            # Broadcast the message to all connected clients
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

    clients.remove(ws)
    return ws

async def handle_signup(request):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return web.HTTPBadRequest()
    await db.add_user(username, password)
    return web.Response(text=f'User {username} successfully signed up', status=200)

async def handle_login(request):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return web.HTTPBadRequest()

    try:
        valid_user = await db.is_user_valid(username, password)
        if valid_user:
            session = await aiohttp_session.new_session(request)
            session['username'] = username
            return web.json_response({'message': 'Login successful'})
        else:
            return web.HTTPUnauthorized(text='Invalid username or password')
    except Exception as e:
        return web.HTTPUnauthorized(text=str(e))

async def init_app():
    await db.init()
    app = web.Application()

    redis_client = redis.from_url("redis://localhost")
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

    for route in list(app.router.routes()):
        cors.add(route)

    return app

if __name__ == '__main__':
    web.run_app(init_app(), host='localhost', port=8080)
