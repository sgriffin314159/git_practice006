# Store text for the post sent to LLM
PROMPT_GENERATE_DRAFT = """
Please write a short social media post for LinkedIn summarizing the following article:
{article_text}
""".strip()