from fastapi import FastAPI
from resources import UserResources

app = FastAPI()

app.include_router(UserResources.router)
@app.get("/")
async def read_root():
    return {'Hello': 'from fastapi boilerplate'}
