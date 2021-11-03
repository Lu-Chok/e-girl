from fastapi import FastAPI

from .waifu_routes import router as waifu_routes_router 


app = FastAPI()

app.include_router(waifu_routes_router.router)
