from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ashinity.core.config import settings
from ashinity.routers import auth, users, properties, inquiries, favorites, paystack, flutterwave
from ashinity.core.db import Base, engine  # <-- import Base and engine
from ashinity import models  # <-- import models so Base knows them

# Create tables at startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ashinity Real Estate API")

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")] if settings.CORS_ORIGINS else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(properties.router)
app.include_router(inquiries.router)
app.include_router(favorites.router)
app.include_router(paystack.router)
app.include_router(flutterwave.router)

@app.get("/")
def root():
    return {"message": "Ashinity Real Estate API"}

