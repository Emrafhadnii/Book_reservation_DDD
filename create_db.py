import asyncpg
from config.setting import settings

async def create():
    try:
        conn = await asyncpg.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            # database="postgres"
            database=settings.DB_NAME
        )
        # await conn.execute('CREATE DATABASE books_db;')
        # await conn.execute('DELETE FROM reservations WHERE id = 12;')
        x = await conn.fetch('SELECT * FROM customers;')
        print(x)
    except asyncpg.DuplicateDatabaseError as e:
        raise Exception(str(e))
    finally:
        if conn is not None:
            await conn.close()

import asyncio
asyncio.run(create())