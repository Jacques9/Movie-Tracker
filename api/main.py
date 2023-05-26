from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import users, movies
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(
        app,
        host = '0.0.0.0',
        port = 8000
    )