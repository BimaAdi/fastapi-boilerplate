from fastapi import FastAPI
from resources import UserResources
from resources import RoleResources
from resources import AuthResources

app = FastAPI()

app.include_router(UserResources.router)
app.include_router(RoleResources.router)
app.include_router(AuthResources.router)
@app.get("/")
async def read_root():
    return {'Hello': 'from fastapi boilerplate'}
