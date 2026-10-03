from fastapi import FastAPI
from fastapi import FastAPI
from app.api.v1.api import api_router

app = FastAPI(title="MXH Giao Duc Truc Tuyen API", version="1.0.0")

# Đăng ký các API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to MXHGDTT API Backend!"}
