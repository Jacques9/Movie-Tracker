from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import users
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    users.router
)

if __name__ == '__main__':
    uvicorn.run(
        'run:app',
        host = '0.0.0.0',
        port = 8000,
        reload=True
    )