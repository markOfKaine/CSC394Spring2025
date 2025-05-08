from fastapi import FastAPI, HTTPException
from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import sqlite3

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("SEEK_API_KEY"), base_url="https://api.deepseek.com/v1")
SQLALCHEMY_DATABASE_URL = "sqlite:///./pubby.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Article(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True

# SQL Alchemy ORM model for articles
class ArticleDB(Base):
    __tablename__ = "articles"
    title = Column(String, primary_key=True, index=True)
    content = Column(String)

Base.metadata.create_all(bind=engine)

articles_list = [
    Article(title="Article324", content="This is an article talking about Spider-man."),
    Article(title="Article325", content="This is an article talking about Daredevil.")]


@app.get("/get-message")
async def read_root():
    return {"Message" : "Congrats! You did it."}

@app.get("/get-articles", response_model=list[Article])
async def getArticles():
    with SessionLocal() as session:
        articles = session.query(ArticleDB).all()
    return articles

@app.post("/add-article", response_model=Article)
async def addArticles(article: Article):
    with SessionLocal() as session:
        articleDB = ArticleDB(**article.dict())
        session.add(articleDB)
        session.commit()
        session.refresh(articleDB)
    return articleDB

@app.delete("/delete-article", response_model=Article)
async def delArticle(articleName: str = ""):
    with SessionLocal() as session:
        article = session.query(ArticleDB).filter(ArticleDB.title == articleName).first()
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        session.delete(article)
        session.commit()
    return article


@app.post("/summarize-article")
async def summarizeArticle(articleName: str = ""):
    with SessionLocal() as session:
        article = session.query(ArticleDB).filter(ArticleDB.title == articleName).first()
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": f"Summarize the following article: {article.content}"}],
            max_tokens=100
        )
        summary = response.choices[0].message.content
        return {"summary": summary}
    return {"message": "Article not found."}
