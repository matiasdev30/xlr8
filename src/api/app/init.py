from fastapi import FastAPI
from api.routes.endpoints import router

xlr8 = FastAPI()


xlr8.include_router(router)
