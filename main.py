from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse, JSONResponse
from api.user_endpoints import user_router

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["users"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)