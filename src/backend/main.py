from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api_routes import shop, save

app = FastAPI(title="NsureCat MVP", version="1.0.0")

# CORS middleware to allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(shop.router, prefix="/v1", tags=["shop"])
app.include_router(save.router, prefix="/v1", tags=["save"])

@app.get("/")
async def root():
    return {"message": "NsureCat MVP API"}