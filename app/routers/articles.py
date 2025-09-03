from fastapi import APIRouter, HTTPException, status
from app.models import Article, User
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleOut
from app.dependencies import db_dep, current_user_jwt_dep

router = APIRouter(
    prefix="/articles",
    tags=["Articles"],
)


# -------------------- Create Article --------------------
@router.post("/", response_model=ArticleOut, status_code=status.HTTP_201_CREATED)
def create_article(
    payload: ArticleCreate,
    db: db_dep,
    current_user: current_user_jwt_dep,
):
    article = Article(**payload.dict(), author_id=current_user.id)
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


# -------------------- Get all published articles (public) --------------------
@router.get("/", response_model=list[ArticleOut])
def list_articles(db: db_dep):
    return db.query(Article).filter(Article.published == True).all()


# -------------------- Get single article --------------------
@router.get("/{article_id}", response_model=ArticleOut)
def get_article(article_id: int, db: db_dep):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


# -------------------- Update article (only owner) --------------------
@router.put("/{article_id}", response_model=ArticleOut)
def update_article(
    article_id: int,
    payload: ArticleUpdate,
    db: db_dep,
    current_user: current_user_jwt_dep,
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(article, key, value)

    db.commit()
    db.refresh(article)
    return article


# -------------------- Delete article (only owner) --------------------
@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: int,
    db: db_dep,
    current_user: current_user_jwt_dep,
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(article)
    db.commit()
    return
