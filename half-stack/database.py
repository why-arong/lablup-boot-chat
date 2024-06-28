# database.py
import asyncpg
import logging
import bcrypt

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, dsn):
        self.dsn = dsn
        self.pool = None

    async def init(self):
        logger.debug('Initializing database connection pool')
        self.pool = await asyncpg.create_pool(dsn=self.dsn)
        await self.create_users_table()
        await self.create_chats_table()

    async def create_chats_table(self):
        logger.debug('Creating chats table if not exists')
        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS chats (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) NOT NULL REFERENCES users(username),
                    content TEXT NOT NULL,
                    timestamp TIMESTAMPTZ DEFAULT NOW()
                )
            ''')

    async def create_users_table(self):
        logger.debug('Creating users table if not exists')
        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            ''')

    async def add_user(self, username, password):
        logger.debug('Adding user to database')
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        async with self.pool.acquire() as conn:
            await conn.execute('''
            INSERT INTO users (username, password) VALUES ($1, $2)
            ''', username, hashed_password)

    async def get_user(self, username):
        logger.debug(f'Fetching user {username} from database')
        async with self.pool.acquire() as conn:
            return await conn.fetchrow('''
            SELECT username, password FROM users WHERE username = $1
            ''', username)

    async def save_chat(self, content, username):
        logger.debug(f'Saving chat: {content}')
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO chats (content, username) VALUES ($1, $2)
            ''', content, username)

    async def get_all_chats(self):
        logger.debug('Fetching all messages from database')
        async with self.pool.acquire() as conn:
            return await conn.fetch('SELECT * FROM chats ORDER BY timestamp ASC')
