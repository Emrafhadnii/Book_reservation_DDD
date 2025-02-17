from fastapi import FastAPI, HTTPException,Depends
from src.entrypoints.getbook import router as book_router
from src.entrypoints.auth import router as auth_router
from src.entrypoints.reservation import router as reserve_router
from contextlib import asynccontextmanager
from src.services_layer.dependencies.otp_dependency import redis_dependency
from src.entrypoints.sign_up import router as signup_router
from src.services_layer.dependencies.bus_dependency import messagebus
from src.services_layer.subscribers import Subscribers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_dependency.connect()
    await messagebus.connect()
    await Subscribers.subs_usercreated(messagebus)

    yield
    
    await messagebus.channel.close()
    await messagebus.connection.close()
    await redis_dependency.disconnect()

app = FastAPI(lifespan=lifespan)


app.include_router(signup_router)
app.include_router(book_router)
app.include_router(auth_router)
app.include_router(reserve_router)



