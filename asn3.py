from fastapi import FastAPI
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.getenv("SEEK_API_KEY"), base_url="https://api.deepseek.com/v1")

articles = {"Article324": "This is an article talking about how Spider-man is better than the following characters in all regards, Daredevil, Punisher, anyone else you would like to name."}

@app.get("/get-message")
async def read_root():
    return {"Message" : "Congrats! You did it."}

@app.get("/get-articles")
async def getArticles():
    return {"Articles" : articles}

@app.post("/add-article")
async def addArticles(articleName: str = "", articleContent: str = ""):
    if articleName not in articles:
        articles[articleName] = articleContent
    return {"Message" : "Article has been added.", "Articles" : articles}

@app.delete("/delete-article")
async def delArticle(articleName: str = ""):
    if articleName in articles.keys():
        articles.remove(articleName)
    return {"message" : "Article has been removed.", "Articles" : articles}

@app.post("/summarize-article")
async def summarizeArticle(articleName: str = ""):
    if articleName in articles.keys():
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": f"Summarize the following article: {articles[articleName]}"}],
            max_tokens=100
        )
        summary = response.choices[0].message.content
        return {"summary": summary}
    else:
        return {"error": f"Article not found."}
