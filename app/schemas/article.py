from datetime import datetime
from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool = True


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None


class ArticleOut(ArticleBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
