from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import ollama

load_dotenv()

# MongoDB Setup
mongo_uri = os.getenv("MONGODB_URI")
mongo_db_name = os.getenv("MONGODB_DB")
mongo_collection_name = os.getenv("MONGO_COLLECTION")

client = MongoClient(mongo_uri)
db = client[mongo_db_name]
collection = db[mongo_collection_name]

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # update this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.post("/query")
async def ask_question(query: Query):
    try:
        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "system", "content": "Answer the user's question in a short and precise manner."},
                {"role": "user", "content": query.question}
            ]
        )
        answer = response["message"]["content"]

        collection.insert_one({
            "question": query.question,
            "answer": answer
        })

        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/conversations")
async def get_conversations():
    try:
        conversations = list(collection.find({}, {"_id": 0}).sort("_id", -1))
        return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not fetch conversations")
@app.delete("/conversations")
def delete_all_conversations():
    result = collection.delete_many({})
    return {"deleted_count": result.deleted_count}
