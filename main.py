from fastapi import FastAPI
from routers import item

app = FastAPI()
app.include_router(item.router)
# app.include_router(auth.router)