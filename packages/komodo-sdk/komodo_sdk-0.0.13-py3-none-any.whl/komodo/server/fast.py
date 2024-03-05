from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from komodo.server import agent_router, appliance_router, conversation_router, user_router
from komodo.server.globals import get_appliance

app = FastAPI()

app.include_router(appliance_router.router)
app.include_router(agent_router.router)
app.include_router(conversation_router.router)
app.include_router(user_router.router)


# Swagger UI: served at /docs.
# ReDoc: served at /redoc.

@app.get("/", tags=["root"])
async def home() -> dict:
    return {'message': "Welcome to Komodo AI Appliance: " + get_appliance().name}


openapi_schema = get_openapi(
    title="Komodo AI Appliance SDK",
    version="0.0.*",
    description="Komodo AI Appliance SDK built using FastAPI",
    routes=app.routes)

app.openapi_schema = openapi_schema

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)  # noinspection PyTypeChecker
