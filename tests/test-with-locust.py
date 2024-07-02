import time
import json
import logging
import asyncio
import websockets
from locust import HttpUser, TaskSet, task, between

logging.basicConfig(level=logging.INFO)

class WebSocketClient:
    def __init__(self, url, session_cookie):
        self.url = url
        self.session_cookie = session_cookie
        self.connection = None

    async def connect(self):
        self.connection = await websockets.connect(self.url, extra_headers={"Cookie": f"AIOHTTP_SESSION={self.session_cookie}"})
        logging.info(f"Connected to {self.url}")

    async def send(self, message):
        await self.connection.send(message)
        logging.info(f"Sent message: {message}")

    async def receive(self):
        response = await self.connection.recv()
        logging.info(f"Received message: {response}")
        return response

    async def close(self):
        await self.connection.close()
        logging.info("Connection closed")

class WebSocketTaskSet(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.session_cookie = None
        self.websocket_client = None

    def on_start(self):
        self.session_cookie = self.login()
        logging.info(f"Session cookie {self.session_cookie}")
        self.websocket_client = WebSocketClient('ws://localhost:8080/ws', self.session_cookie)
        self.loop.run_until_complete(self.websocket_client.connect())
        self.loop.create_task(self.receive_messages())

    def on_stop(self):
        self.loop.run_until_complete(self.websocket_client.close())

    def login(self):
        response = self.client.post("/login", json={"username": "test_user", "password": "test_password"})
        if response.status_code == 200:
            logging.info("User logged in successfully")
            return response.cookies["AIOHTTP_SESSION"]
        else:
            logging.error("User login failed")
            return None

    async def receive_messages(self):
        while True:
            try:
                response = await self.websocket_client.receive()
                logging.info(f"Received chat message: {response}")
            except websockets.exceptions.ConnectionClosedError as e:
                logging.warning(f"WebSocket connection closed: {e}, reconnecting...")
                await self.websocket_client.connect()
            except Exception as e:
                logging.error(f"Error receiving message: {e}")

    @task
    def send_and_receive(self):
        self.loop.run_until_complete(self.send_chat_message())

    async def send_chat_message(self):
        try:
            message = json.dumps({"content": "Hello from Locust", "timestamp": time.time()})
            await self.websocket_client.send(message)
            logging.info(f"Sent chat message: {message}")
        except websockets.exceptions.ConnectionClosedError as e:
            logging.warning(f"WebSocket connection closed while sending: {e}, reconnecting...")
            await self.websocket_client.connect()
            await self.websocket_client.send(message)

class WebSocketLocust(HttpUser):
    tasks = [WebSocketTaskSet]
    wait_time = between(1, 2)
    host = "http://localhost:8080"
