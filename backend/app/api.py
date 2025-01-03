from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from backend.app.routes import products, recognize

app = FastAPI(docs_url="/api/docs", title="Smart Scales API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(recognize.router)