import asyncpg
from config.setting import settings

async def insert():
    try:
        conn = await asyncpg.connect(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            database=settings.DB_NAME
        )
        with open('/app/setup_db/sample.sql', 'r') as file:
            sql = file.read()
        await conn.execute(sql)
    except Exception as e:
        print(f"There are some errors:{e}")
    finally:
        await conn.close()
import asyncio
asyncio.run(insert())
