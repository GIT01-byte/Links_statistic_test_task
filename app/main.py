from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from db.orm import AsyncOrm

from api.links import router as links_router

from models.links import setup_admin
from db.session import async_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    await AsyncOrm.create_tables() 
    print('INFO:     База перезапущена')
    yield
    print('INFO:     Выключение...')


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
)

app.include_router(links_router)

setup_admin(app, async_engine)

if __name__ == '__main__':
    uvicorn.run(f'{__name__}:app', reload=True)
