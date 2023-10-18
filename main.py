from fastapi import FastAPI
from api.user_endpoints import user_endpoints

app = FastAPI()

app.include_router(user_endpoints)
