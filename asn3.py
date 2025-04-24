from fastapi import FastAPI
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.deepseek.com/v1")

articles = ["Article324", "Article1234 is about computer science and how it is used in the world today."]

@app.get("/get-message")
async def read_root():
    return {"Message" : "Congrats! You did it."}

@app.get("/get-articles")
async def getArticles():
    return {"Message" : articles}

@app.post("/add-article")
async def addArticles(article: str = ""):
    if article not in articles:
        articles.append(article)
    return {"Message" : "Article has been added.", "Articles" : articles}

@app.delete("/delete-article")
async def delArticle(article: str = ""):
    if article in articles:
        articles.remove(article)
    return {"message" : "Article has been removed.", "Articles" : articles}

@app.post("/summarize-article")
async def summarizeArticle(article: str = ""):
    if article in articles:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": f"Summarize the following article: {article}"}],
            max_tokens=100
        )
        summary = response.choices[0].message.content
        return {"summary": summary}
    else:
        return {"error": "Article not found."}
