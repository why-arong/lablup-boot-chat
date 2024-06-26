import aiohttp
import aiohttp.web as web
import aiohttp_cors
from database import Database

clients = []
db = Database(dsn='postgresql://postgres:abc@localhost/postgres')


async def handle_websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    clients.append(ws)

    # Send existing messages to the newly connected client
    messages = await db.get_all_chats()
    for message in messages:
        await ws.send_str(message['content'])

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            await db.save_chat(msg.data)
            # Broadcast the message to all connected clients
            for client in clients:
                if client.closed:
                    clients.remove(client)
                else:
                    await client.send_str(msg.data)
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
        user_validation = await db.is_user_valid(username, password)
        if user_validation:
            return web.Response(text=f'User {username} successfully logged in', status=200)
        else:
            return web.HTTPUnauthorized(text='Invalid username or password')
    except Exception as e:
        return web.HTTPUnauthorized(text=str(e))


async def init_app():
    await db.init()
    app = web.Application()
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
