import asyncio


class ChatServer:
    def __init__(self):
        self.clients = []

    async def handle_client(self, reader, writer):
        client = writer.get_extra_info('peername')
        self.clients.append(writer)
        print(f"{client} has connected.")

        try:
            while True:
                data = await reader.read(100)
                message = data.decode()
                if not message:
                    break
                print(f"Received message from {client}: {message}")
                await self.broadcast_message(message, writer)
        except asyncio.CancelledError:
            pass
        finally:
            print(f"{client} has disconnected.")
            self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()

    async def broadcast_message(self, message, sender):
        for client in self.clients:
            if client != sender:
                client.write(message.encode())
                await client.drain()

    async def run_server(self, host='127.0.0.1', port=8888):
        server = await asyncio.start_server(self.handle_client, host, port)
        async with server:
            await server.serve_forever()


if __name__ == '__main__':
    chat_server = ChatServer()
    asyncio.run(chat_server.run_server())
