import aiohttp
import aiohttp.web as web
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


async def init_app():
    await db.init()
    app = web.Application()
    app.router.add_get('/ws', handle_websocket)
    return app

if __name__ == '__main__':
    web.run_app(init_app(), host='localhost', port=8080)
