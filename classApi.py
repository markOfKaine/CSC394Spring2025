from fastapi import FastAPI

##this api was the one we used in class
##for this assignment I think this would suffice, for the project we are using django

app = FastAPI()

articles = ["Article324"]
users = ["Article324"]
notes = [""]

@app.get("/get-message")
async def read_root():
    return {"Message" : "Congrats! You did it."}

@app.get("/get-articles")
async def getArticles():
    return {"Message" : articles}

@app.get("/get-users")
async def getUsers():
    return {"Message" : users}

@app.get("/get-notes")
async def getNotes():
    return {"Message" : notes}

@app.post("/add-article")
async def addArticles(article: str = ""):
    if article not in articles:
        articles.append(article)
    return {"Message" : "Article has been added.", "Articles" : articles}

@app.post("/add-user")
async def addUser(user: str = ""):
    if user not in users:
        users.append(user)
    return {"Message" : "User has been added.", "Users" : users}

@app.post("/add-notes")
async def addNotes(note: str = ""):
    if note not in notes:
        notes.append(note)
    return {"Message" : "Note has been added.", "notes" : notes}

@app.delete("/delete-article")
async def delArticle(article: str = ""):
    if article in articles:
        articles.remove(article)
    return {"message" : "Article has been removed.", "Articles" : articles}

@app.delete("/delete-user")
async def delUser(user: str = ""):
    if user in users:
        users.remove(user)
    return {"message" : "User has been removed.", "Users" : users}

@app.delete("/delete-note")
async def delNote(note: str = ""):
    if note in notes:
        notes.remove(note)
    return {"message" : "Note has been removed.", "Notes" : notes}
