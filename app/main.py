# main.py containing FastAPI object, post, and get

import asyncio
import uvicorn
from fastapi import FastAPI, Body
from openai_client import client
from post_generator import generate_post
from storage import load_data, save_data


app = FastAPI()

"""
     POST endpoint to generate social media drafts from an article's text.
     Accepts article text and optional number of drafts to generate.
     Defaults to 3 drafts if not specified.
     Args:
         article_text (str): The text of the article to summarize.
         num_posts (int): The number of social media posts to generate. 
"""
# Asynchronous function that calls OpenAI to generate a post
@app.post("/generate-posts")
async def generate_posts(article_text: str = Body(...),
                         num_posts: int = Body(3)):
    tasks = [asyncio.create_task(generate_post(article_text)) for _ in range(num_posts)]      
    drafts = await asyncio.gather(*tasks)

    data = load_data()
    data.append({"article_text": article_text, "drafts": drafts})

    save_data(data)

    return {"drafts": drafts}



"""
    GET endpoint to retrieve all stored articles and generate draft posts.
"""   
@app.get("/posts")
def get_posts():
    return load_data()


# Let's run this app!
if __name__ == "__main__":
    # Run the server on localhost:8000
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


