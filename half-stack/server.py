import aiohttp
import aiohttp.web as web
import aiohttp_cors
import aiohttp_session
import aiohttp_session.redis_storage
from database import Database
import redis.asyncio as redis
import json
from datetime import datetime
import bcrypt
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:abc@db:5432/postgres')
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379')
clients = []
db = Database(dsn=DATABASE_URL)


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
                logger.error(f'WebSocket connection closed with exception {ws.exception()}')
    finally:
        clients.remove(ws)

    return ws


async def handle_signup(request):
    try:
        data = await request.json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            logger.warning('Signup request missing username or password')
            return web.HTTPBadRequest(text='Missing username or password')

        await db.add_user(username, password)
        logger.info(f'User {username} successfully signed up')
        return web.Response(text=f'User {username} successfully signed up', status=200)
    except Exception as e:
        logger.error(f'Error during signup: {e}')
        return web.HTTPInternalServerError(text=str(e))


async def handle_login(request):
    try:
        data = await request.json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            logger.warning('Login request missing username or password')
            return web.HTTPBadRequest(text='Missing username or password')

        user = await db.get_user(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session = await aiohttp_session.new_session(request)
            session['username'] = username
            logger.info(f'User {username} logged in successfully')
            return web.json_response({'message': 'Login successful'})
        else:
            logger.warning(f'Invalid login attempt for user {username}')
            return web.HTTPUnauthorized(text='Invalid username or password')
    except Exception as e:
        logger.error(f'Error during login: {e}')
        return web.HTTPUnauthorized(text=str(e))


async def init_app():
    try:
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

        for route in list(app.router.routes()):
            cors.add(route)

        logger.info('Application initialized successfully')
        return app
    except Exception as e:
        logger.error(f"Failed to initialize app: {e}")
        raise


if __name__ == '__main__':
    web.run_app(init_app(), host='0.0.0.0', port=8080)
