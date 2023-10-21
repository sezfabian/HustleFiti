from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse, JSONResponse, RedirectResponse
from fastapi.openapi.utils import get_openapi
from api.user_endpoints import user_router
from api.service_endpoints import service_router
from api.contract_endpoints import contract_router
from api.payment_endpoints import payment_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(swagger_ui_parameters={"deepLinking": True,})



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify the allowed origins as a list of strings
    allow_credentials=True,
    allow_methods=["*"],  # Specify the allowed HTTP methods as a list of strings
    allow_headers=["*"],  # Specify the allowed HTTP headers as a list of strings
)

app.include_router(user_router, prefix="/user", tags=["users"])
app.include_router(service_router, prefix="", tags=["services"])
app.include_router(contract_router, prefix="/contract", tags=["contracts"])
app.include_router(payment_router, prefix="/payment", tags=["payments"])

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="HustleFiti_API",
        version="1.0.0",
        summary="An api for HustleFiti app",
        description="An Online Marketplace for short term contract services",
        terms_of_service="https://www.google.com/policies/terms/",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://i.postimg.cc/GtCK63Cr/logo.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Route for the root path ("/") to redirect to Redoc documentation
@app.get("/", response_class=RedirectResponse, tags=["documentation"])
async def redoc():
    # Redirect to the Redoc endpoint
    return "/redoc"

# Route for the root path ("/docs") to redirect to Swagger documentation
@app.get("/docs", response_class=RedirectResponse, tags=["documentation"])
async def docs():
    # Redirect to the Redoc endpoint
    return "/docs"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)