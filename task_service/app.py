from fastapi import FastAPI
from schema.schema import graphql_app
from models.models import database
from database.database import _async_main

app = FastAPI()

@app.get("/")
def read_root():
    return {"GraphQL": "/graphql"}


app.include_router(graphql_app, prefix='/graphql')


@app.on_event("startup")
async def on_startup():
    await _async_main()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
