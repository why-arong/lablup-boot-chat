# Real-Time Multi-User Chat Application

This project is a real-time multi-user chat application built using Python and aio libraries. The application supports user sign-up, login, and real-time chat functionality using WebSockets. The application is containerized using Docker and Docker Compose for easy setup and deployment.

## Features

- User sign-up and login
- Real-time messaging with WebSocket
- Message broadcasting to all connected clients
- Persistent storage of messages using PostgreSQL
- Session management using Redis

## Requirements

- Docker
- Docker compose

## Setup

1. **Clone the Repository:**

    ```sh
    git clone https://github.com/why-arong/lablup-boot-chat.git
    cd lablup-boot-chat
    ```

2. **Create `.env` File:**

    Create a `.env` file in the root directory of your project and add the following environment variables:

    ```env
    DATABASE_URL=postgresql://{user}:{password}@db:{port}/{database
    REDIS_URL=redis://redis:6379
    ```

3. **Build and Run the Application:**

    Use Docker Compose to build the images and start the containers:

    ```sh
    docker-compose up --build
    ```

    This will start the following services:
    - `web`: The Python web application
    - `db`: PostgreSQL database
    - `redis`: Redis server

## Usage

### Accessing the Application

Once the containers are up and running, you can access the application at `http://localhost:8080`.



## Development

### Running Tests


