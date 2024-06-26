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
                user_id INT NOT NULL REFERENCES users(id),
                content TEXT NOT NULL,
                timestamp TIMESTAMPTZ DEFAULT NOW()
            )
        ''')

    async def create_users_table(self):
        logger.debug('Creating users table if not exists')
        await self.conn.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR NOT NULL,
                        password VARCHAR NOT NULL
                    )
                ''')

    async def add_user(self, username, password):
        logger.debug('Adding user to database')
        await self.conn.execute('''
        INSERT INTO users (username, password) VALUES ($1, $2)
        ''', username, password)

    async def is_user_valid(self, username, password):
        logger.debug(f'Check if user valid {username}, {password}')
        status = await self.conn.execute('''
        SELECT * FROM users WHERE username = $1 AND password = $2
        ''', username, password)
        return True if int(status[-1]) else False

    async def save_chat(self, content, user_id):
        logger.debug(f'Saving chats: {content}')
        await self.conn.execute('''
            INSERT INTO chats (content) VALUES ($1)
        ''', content)

    async def get_all_chats(self):
        logger.debug('Fetching all messages from database')
        return await self.conn.fetch('SELECT * FROM chats ORDER BY timestamp ASC')
