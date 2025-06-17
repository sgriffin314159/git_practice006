import os
import json
import asyncio
from typing import List
from fastapi import FastAPI
from fastapi import Body
import uvicorn
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Initialize OpenAI client (v1.x.x)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY") )

app = FastAPI()

DATA_FILE = "data.json"

PROMPT_GENERATE_DRAFT = """
Please write a short social media post for LinkedIn summarizing the following article:

{article_text}
""".strip()

# Helper function to load JSON data
def load_data() -> List[dict]:
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Helper function to save JSON data
def save_data(data: List[dict]):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Asynchronous function that calls OpenAI to generate a post
async def generate_post(article_text: str) -> str:
    prompt = PROMPT_GENERATE_DRAFT.format(article_text=article_text)
    chat_completion = await asyncio.to_thread(client.chat.completions.create,
        messages=[{"role": "user", "content": prompt}],
        model="gpt-4.1-mini-2025-04-14",)
    return chat_completion.choices[0].message.content.strip()

@app.post("/generate-posts")
async def generate_posts(
			article_text: str = Body(...),
			num_posts: int = Body(3)):
    """
    Receives article text, generates three social media posts asynchronously,
    saves them to data.json, and returns the drafts.
    """
    # Prepare tasks for concurrency
    tasks = [asyncio.create_task(generate_post(article_text)) for _ in range(num_posts)]
    drafts = await asyncio.gather(*tasks)

    # Load existing data
    data = load_data()

    # Add new entry
    new_entry = {
        "article_text": article_text,
        "drafts": drafts
    }
    data.append(new_entry)

    # Save updated data
    save_data(data)

    return {"drafts": drafts}

@app.get("/posts")
def get_posts():
    """
    Returns all stored articles and draft posts from data.json.
    """
    return load_data()

if __name__ == "__main__":
    # Run the server on localhost:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
