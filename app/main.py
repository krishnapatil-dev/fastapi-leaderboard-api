from fastapi import FastAPI
from app.routes.leaderboard import router
from app.database import init_db

app = FastAPI()
app.include_router(router)


init_db()