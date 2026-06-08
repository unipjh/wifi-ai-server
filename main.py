from fastapi import FastAPI

from app.api.routes.degradation import router as degradation_router
from app.api.routes.recommendation import router as recommendation_router

app = FastAPI(title="Wi-Fi Rec AI Server")
app.include_router(degradation_router, prefix="/api/v1")
app.include_router(recommendation_router, prefix="/api/v1")
