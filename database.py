import asyncpg
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Database:
    def __init__(self, dsn):
        self.dsn = dsn

    async def init(self):
        logger.debug('Initializing database connection')
        self.conn = await asyncpg.connect(self.dsn)
        await self.create_users_table()
        await self.create_chats_table()

    async def create_chats_table(self):
        logger.debug('Creating chats table if not exists')
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL REFERENCES users(username),
                content TEXT NOT NULL,
                timestamp TIMESTAMPTZ DEFAULT NOW()
            )
        ''')

    async def create_users_table(self):
        logger.debug('Creating users table if not exists')
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) UNIQUE NOT NULL
            )
        ''')

    async def add_user(self, username, password):
        logger.debug('Adding user to database')
        await self.conn.execute('''
        INSERT INTO users (username, password) VALUES ($1, $2)
        ''', username, password)

    async def is_user_valid(self, username, password):
        logger.debug(f'Check if user valid {username}')
        user = await self.conn.fetchrow('''
        SELECT username FROM users WHERE username = $1 AND password = $2
        ''', username, password)
        return user['username'] if user else None

    async def save_chat(self, content, username):
        logger.debug(f'Saving chat: {content}')
        await self.conn.execute('''
            INSERT INTO chats (content, username) VALUES ($1, $2)
        ''', content, username)

    async def get_all_chats(self):
        logger.debug('Fetching all messages from database')
        return await self.conn.fetch('SELECT * FROM chats ORDER BY timestamp ASC')
