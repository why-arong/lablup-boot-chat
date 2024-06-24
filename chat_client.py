import asyncio

async def handle_server(reader, writer):
    async def send_message():
        while True:
            message = input("> ")
            writer.write(message.encode())
            await writer.drain()

    async def receive_message():
        while True:
            data = await reader.read(100)
            message = data.decode()
            if not message:
                break
            print(f"\n{message}\n> ", end='')

    await asyncio.gather(send_message(), receive_message())

async def main():
    host = '127.0.0.1'
    port = 8888
    reader, writer = await asyncio.open_connection(host, port)
    print(f"Connected to chat server at {host}:{port}")
    await handle_server(reader, writer)

if __name__ == '__main__':
    asyncio.run(main())
