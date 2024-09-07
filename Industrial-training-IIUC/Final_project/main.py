from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, Base, Category, Image, News, Publisher, Reporter, Summary
from pydantic import BaseModel
from typing import List
import uvicorn
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from bangla_summarizer import summarize

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define the model for the POST request
class NewsInput(BaseModel):
    url: str
"""
# POST endpoint to add a news article
@app.post("/news/")
async def post_news(news_input: NewsInput, db: Session = Depends(get_db)):
    url = news_input.url

    try:
        # Scrape the news article
        article = Article(url)
        article.download()
        article.parse()

        title = article.title
        body = article.text
        author = article.authors[0] if article.authors else "Unknown"
        image_url = article.top_image  # You can adjust this depending on your needs

        # Additional metadata (dummy values for now)
        category_id = 1  # You might want to implement logic to categorize the article
        time_date = article.publish_date if article.publish_date else "2023-09-01T00:00:00"

        # Insert the data into the database
        news = News(
            category_id=category_id,
            author_id=1,  # Dummy author_id for now
            editor_id=1,  # Dummy editor_id for now
            datetime=time_date,
            title=title,
            body=body,
            link=url
        )
        db.add(news)
        db.commit()
        db.refresh(news)

        image = Image(news_id=news.id, image_url=image_url)
        db.add(image)
        db.commit()

        return {"message": "News article successfully posted", "news_id": news.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""
# GET endpoint to fetch a summary of the news by ID
@app.get("/news/{news_id}/summary")
def get_news_summary(news_id: int, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    
    # Placeholder summary logic - replace with actual summarization
    summary_text = summarize(news.body)  # Replace with real summarization logic

    # Save the summary in the database
    summary = Summary(news_id=news_id, summary_text=summary_text)
    db.add(summary)
    db.commit()
    db.refresh(summary)

    return {"news_id": news_id, "summary": summary_text}

# Other existing endpoints
@app.get("/categories/")
def read_categories(db: Session = Depends(get_db)):
    return [{"id": category.id, "name": category.name} for category in db.query(Category).all()]

@app.get("/images/")
def read_images(db: Session = Depends(get_db)):
    return [{"id": image.id, "url": image.image_url} for image in db.query(Image).all()]

@app.get("/news/")
def read_news(db: Session = Depends(get_db)):
    return [{"id": news.id, "title": news.title, "content": news.body} for news in db.query(News).all()]

@app.get("/news/{news_id}")
def read_news_by_id(news_id: int, db: Session = Depends(get_db)):
    news = db.query(News).filter_by(id=news_id).first()
    if news:
        return {"id": news.id, "title": news.title, "content": news.body}
    else:
        raise HTTPException(status_code=404, detail="News not found")

@app.get("/publisher/")
def read_publisher(db: Session = Depends(get_db)):
    return [{"id": publisher.id, "name": publisher.name} for publisher in db.query(Publisher).all()]

@app.get("/reporter/")
def read_reporter(db: Session = Depends(get_db)):
    return [{"id": reporter.id, "name": reporter.name} for reporter in db.query(Reporter).all()]

@app.get("/summaries/")
def read_summaries(db: Session = Depends(get_db)):
    return [{"id": summary.id, "text": summary.summary_text} for summary in db.query(Summary).all()]

@app.get("/")
def welcome():
    return {"message": "I'm up and running!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
