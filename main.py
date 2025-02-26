from fastapi import FastAPI
from src.auth.entrypoints.auth import router as auth_router
from src.reservations.entrypoints.reservation import router as reserve_router
from contextlib import asynccontextmanager
from src.auth.entrypoints.dependencies.otp_dependency import redis_dependency
from src.auth.entrypoints.sign_up import router as signup_router
from src.services_layer.bus_dependency import messagebus
from src.services_layer.consumers import Consumers
from src.books.entrypoints.book_router import router as book_router
from src.users.entrypoints.user_router import router as user_router
from src.users.entrypoints.customer_router import router as customer_router
from src.reservations.entrypoints.reservation_router import router as reservation_router
from BackgroundWorkers.notification import send_notification
from BackgroundWorkers.outbox_listener import outbox_event_listener
import asyncio
from src.adapters.Mongo_DB import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_dependency.connect()
    await messagebus.connect()
    await Consumers.comsuming_queues(messagebus)
    asyncio.create_task(send_notification())
    await db['books'].create_index([('title', 'text')], default_language='english')
    asyncio.create_task(outbox_event_listener())

    yield
    
    await messagebus.channel.close()
    await messagebus.connection.close()
    await redis_dependency.disconnect()

app = FastAPI(lifespan=lifespan)


app.include_router(signup_router)
app.include_router(book_router)
app.include_router(auth_router)
app.include_router(reserve_router)
app.include_router(user_router)
app.include_router(customer_router)
app.include_router(reservation_router)

