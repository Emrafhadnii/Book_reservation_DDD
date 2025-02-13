from fastapi import FastAPI, HTTPException,Depends
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from src.entrypoints.getbook import router as book_router
from src.entrypoints.auth import router

app = FastAPI()

app.include_router(book_router)
app.include_router(router)




