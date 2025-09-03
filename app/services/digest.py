import json
from datetime import datetime
from app.models import Article


def generate_weekly_digest(db, filepath="weekly_digest.json"):
    
    articles = db.query(Article).filter(Article.published == True).all()
    digest = [
        {
            "id": a.id,
            "title": a.title,
            "created_at": a.created_at.isoformat()
        }
        for a in articles
    ]

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({
            "generated_at": datetime.now().isoformat(),
            "articles": digest
        }, f, indent=4, ensure_ascii=False)

    return filepath
