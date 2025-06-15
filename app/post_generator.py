# Sends prompt and article to LLM
# 
from .openai_client import client
from .prompts import PROMPT_GENERATE_DRAFT
import asyncio


async def generate_post(article_text: str) -> str:
    """
    Generates a social media post draft using the provided article text.
    
    Args:
        article_text (str): The text of the article to summarize.
        
    Returns:
        str: The generated social media post draft.
    """
    prompt = PROMPT_GENERATE_DRAFT.format(article_text=article_text)
    
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that writes social media posts."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()