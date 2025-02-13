import asyncpg
from config.setting import settings

async def create():
    try:
        conn = await asyncpg.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            database="postgres"
        )
        # await conn.execute('SELECT users.id, users.username, users.first_name, users.last_name, users.phone, users.email, users.user_password, users.user_role FROM users WHERE users.email = "customer4@example.com"')
        await conn.execute('CREATE DATABASE books_db;')
        # print("Database 'books_db' created successfully.")
    except asyncpg.DuplicateDatabaseError as e:
        raise Exception(str(e))
    finally:
        if conn is not None:
            await conn.close()

import asyncio
asyncio.run(create())