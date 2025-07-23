from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pymongo import MongoClient
import uvicorn
import certifi
import logging

import os
import ollama

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)

# MongoDB Setup
mongo_uri = os.getenv("MONGODB_URI")
mongo_db_name = os.getenv("MONGODB_DB")
mongo_collection_name = os.getenv("MONGO_COLLECTION")

if not all([mongo_uri, mongo_db_name, mongo_collection_name]):
    logging.error("MongoDB environment variables not set.")
    raise RuntimeError("Missing MongoDB environment variables.")

try:
    client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
    db = client[mongo_db_name]
    collection = db[mongo_collection_name]
except Exception as e:
    logging.exception("Failed to connect to MongoDB")
    raise RuntimeError("MongoDB connection failed") from e

# FastAPI setup
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class Query(BaseModel):
    question: str

# Routes
@app.post("/query")
async def ask_question(query: Query):
    try:
        logging.info(f"Received question: {query.question}")
        
        response = ollama.chat(
            model="mistral",
            messages=[
                {"role": "system", "content": "Answer the user's question in a short and precise manner."},
                {"role": "user", "content": query.question}
            ]
        )

        answer = response.get("message", {}).get("content")
        if not answer:
            logging.error("No content in Ollama response")
            raise HTTPException(status_code=500, detail="No content from model")

        collection.insert_one({
            "question": query.question,
            "answer": answer
        })

        return {"answer": answer}
    except Exception as e:
        logging.exception("Error in /query endpoint")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/conversations")
async def get_conversations():
    try:
        conversations = list(collection.find({}, {"_id": 0}).sort("_id", -1))
        return conversations
    except Exception as e:
        logging.exception("Error in /conversations GET")
        raise HTTPException(status_code=500, detail="Could not fetch conversations")

@app.delete("/conversations")
def delete_all_conversations():
    try:
        result = collection.delete_many({})
        return {"deleted_count": result.deleted_count}
    except Exception as e:
        logging.exception("Error in /conversations DELETE")
        raise HTTPException(status_code=500, detail="Could not delete conversations")

# Uvicorn entry point
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

