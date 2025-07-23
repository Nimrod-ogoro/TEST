from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pymongo import MongoClient
import uvicorn
import certifi
import logging
import os
import requests

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
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class Query(BaseModel):
    question: str

# Grok (xAI) API setup
GROK_API_KEY = os.getenv("GROK_API_KEY")

def query_grok(question: str):
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [
            {"role": "system", "content": "Answer the question accurately and concisely."},
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",  # Example endpoint
            headers=headers,
            json={
                "model": "mixtral-8x7b-32768",
                "messages": payload["messages"],
                "temperature": 0.7
            }
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        logging.exception("Error communicating with Grok API")
        raise

# Routes
@app.post("/query")
async def ask_question(query: Query):
    try:
        logging.info(f"Question: {query.question}")
        answer = query_grok(query.question)

        collection.insert_one({
            "question": query.question,
            "answer": answer
        })

        return {"answer": answer}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to process query")

@app.get("/conversations")
async def get_conversations():
    try:
        conversations = list(collection.find({}, {"_id": 0}).sort("_id", -1))
        return conversations
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch conversations")

@app.delete("/conversations")
async def delete_conversations():
    try:
        result = collection.delete_many({})
        return {"deleted_count": result.deleted_count}
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete conversations")

# Run the server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)


