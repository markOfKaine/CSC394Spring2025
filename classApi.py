from fastapi import FastAPI

app = FastAPI()

articles = ["Article324"]

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
