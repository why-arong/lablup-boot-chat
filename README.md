# Real-time Multi-user Chat Application

This is a real-time, multi-user chat application built using Python, aiohttp, and Redis for the backend, and React for the frontend. The application supports user authentication, real-time messaging, and persistent chat history.

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
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Set up environment variables:**

   Create a `.env` file in the root directory and add the following environment variables:

   ```env
   DATABASE_URL=postgresql://postgres:abc@db:5432/postgres
   REDIS_URL=redis://redis:6379
   ```

3. **Build and run the containers:**

   ```sh
   docker-compose up --build
   ```

4. **Access the application:**

   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8080](http://localhost:8080)

## Usage

### Sign Up

1. Go to [http://localhost:3000](http://localhost:3000).
2. Click on the "Sign Up" link.
3. Enter a username and password.
4. Click "Sign Up".

### Login

1. Go to [http://localhost:3000](http://localhost:3000).
2. Enter your username and password.
3. Click "Login".

### Chat

1. After logging in, you will be redirected to the chat page.
2. Enter a message in the input field and press "Send".
3. The message will be broadcast to all connected users in real-time.
