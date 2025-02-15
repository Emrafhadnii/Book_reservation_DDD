from fastapi import FastAPI, HTTPException,Depends
from src.entrypoints.getbook import router as book_router
from src.entrypoints.auth import router
from src.entrypoints.reservation import router as reserve_route


app = FastAPI()

app.include_router(book_router)
app.include_router(router)
app.include_router(reserve_route)



