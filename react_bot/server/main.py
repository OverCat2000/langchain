from fastapi import FastAPI
from pydantic import BaseModel
import openai
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
from myAgent import run_agent

# Set up your OpenAI API key securely
openai.api_key = os.environ['OPENAI_API_KEY']

def process_message(message: str) -> str:
    # client = OpenAI()
    # response = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "user", "content": message}
    #     ]
    # )
    response = run_agent(message)
    print(response['chat_history'][1].content)
    return response['chat_history'][1].content

app = FastAPI()

class Query(BaseModel):
    message: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add other origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chatbot/")
async def get_response(query: Query):
    response = process_message(query.message)
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
