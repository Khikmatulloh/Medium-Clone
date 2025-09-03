from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from app.models import User, Article
from app.dependencies import db_dep,get_current_admin_from_cookie
from app import utils

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


# Admin login (cookie auth)
@router.post("/login")
def admin_login(username: str, password: str, response: Response, db: Session = Depends(db_dep)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not utils.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Not an admin")

    token = utils.create_jwt_token(data={"sub": user.username, "role": "admin"}, expires_delta=60)
    utils.set_admin_cookie(response, token)

    return {"msg": "Admin logged in successfully"}


# Admin logout
@router.post("/logout")
def admin_logout(response: Response):
    utils.clear_admin_cookie(response)
    return {"msg": "Logged out"}


# Manage users
@router.get("/users")
def list_users(db: Session = Depends(db_dep), current_admin=Depends(get_current_admin_from_cookie)):
    return db.query(User).all()


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(db_dep), current_admin=Depends(get_current_admin_from_cookie)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"msg": "User deleted"}


# Manage articles
@router.get("/articles")
def list_articles(db: Session = Depends(db_dep), current_admin=Depends(get_current_admin_from_cookie)):
    return db.query(Article).all()


@router.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(db_dep), current_admin=Depends(get_current_admin_from_cookie)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(article)
    db.commit()
    return {"msg": "Article deleted"}
