from fastapi import FastAPI, HTTPException,Depends
from src.entrypoints.auth import router as auth_router
from src.entrypoints.reservation import router as reserve_router
from contextlib import asynccontextmanager
from src.services_layer.dependencies.otp_dependency import redis_dependency
from src.entrypoints.sign_up import router as signup_router
from src.services_layer.dependencies.bus_dependency import messagebus
from src.services_layer.consumers import Consumers
from src.entrypoints.book_router import router as book_router
from src.entrypoints.user_router import router as user_router
from src.entrypoints.customer_router import router as customer_router
from src.entrypoints.reservation_router import router as reservation_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_dependency.connect()
    await messagebus.connect()
    await Consumers.comsuming_queues(messagebus)

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

