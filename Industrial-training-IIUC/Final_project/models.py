# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel
from typing import Optional


class Category(BaseModel):
    id: int
    name: str
    description: str

class Image(BaseModel):
    id: int
    news_id: int
    image_url: str

class News(BaseModel):
    id: int
    category_id: int
    author_id: int
    editor_id: int
    datetime: str
    title: str
    body: str
    link: str

class Publisher(BaseModel):
    id: int
    name: str
    email: str
    phone_number: str
    head_office_address: str
    website: str
    facebook: str
    twitter: str
    linkedin: str
    instagram: str

class Reporter(BaseModel):
    id: int
    name: str
    email: str

class Summary(BaseModel):
    id: int
    news_id: int
    summary_text: str