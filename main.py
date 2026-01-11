from typing import Annotated
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_crudrouter_mongodb import CRUDRouter, MongoModel, ObjectId, MongoObjectId
import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URL"))
db = client.tododb

# Model (using MongoModel instead of Beanie)
class Todo(MongoModel):
    id: Annotated[ObjectId, MongoObjectId] | None = None
    title: str
    completed: bool = False

# Create FastAPI app
app = FastAPI(title="Todo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 THE MAGIC - CRUDRouter (like Django ViewSet!)
router = CRUDRouter(
    model=Todo,
    db=db,
    collection_name="todos",
    prefix="/todos",
    tags=["todos"]
)

app.include_router(router)