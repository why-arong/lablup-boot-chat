# Real-time Multi-user Chat Application

This is a real-time, multi-user chat application built using aiohttp, asyncpg and Redis for the backend, and React for the frontend. The application supports user authentication, real-time messaging, and persistent chat history.

## Features

- User sign-up and login
- Real-time messaging with WebSocket
- Persistent chat history
- Dockerized for easy deployment


## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/why-arong/lablup-boot-chat.git
   cd lablup-boot-chat
   ```


2. **Build and run the containers:**

   ```sh
   docker-compose up --build
   ```

4. **Access the application:**
   - Open your browser and navigate to http://localhost:3000.


# Running Tests

### Load Testing with Locust

**Install Locust:**
```sh
pip install locust
```

**Run Locust:**
```sh
locust -f tests/test-with-locust.py --host=http://localhost:8080
```
Access the Locust web interface at http://localhost:8089 to start the load tests.

### Test using `asyncio`
```shell
python tests/test-send-messages.py
```


## Caution ‼️

When deploying the application, you need to update the environment variables in the `.env` file to match the production environment. 
For example:
```.env
// for server-side env (half-stack)
DATABASE_URL=postgresql://postgres:yourpassword@yourproductiondb:5432/yourproductiondb
REDIS_URL=redis://yourproductionredis:6379

// for client-side env (chat-ui)
REACT_APP_API_URL=https://yourproductionapi.com
REACT_APP_WS_URL=wss://yourproductionapi.com/ws
```