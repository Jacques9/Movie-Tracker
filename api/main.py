from fastapi import FastAPI
from .routes import users, movies
import uvicorn

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run(
        app,
        host = '0.0.0.0',
        port = 8000
    )