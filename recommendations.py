import models
from models import Users, Announcements, Favorite, ViewedAnnouncements
from sqlalchemy.orm import Session
from database import SessionLocal
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter(
    prefix='/recommendations',
    tags=['recommendations_list']
)


def get_recommendations(user_id: int, db: Session, num_recommendations: int = 10):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        return []

    # Fetch all announcements
    announcements = db.query(Announcements).all()
    if not announcements:
        return []

    # Prepare data for TF-IDF
    announcement_ids = [announcement.id for announcement in announcements]
    announcement_titles = [announcement.title for announcement in announcements]
    announcement_descriptions = [announcement.description for announcement in announcements]

    combined_text = [f"{title} {desc}" for title, desc in zip(announcement_titles, announcement_descriptions)]

    # Vectorize text
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(combined_text)
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get user's viewed announcements
    # user_announcements = db.query(Announcements).filter(Announcements.user_id == user_id).all()
    user_favorites = db.query(Favorite).filter(Favorite.user_id == user_id).all()
    user_clicks = db.query(ViewedAnnouncements).filter(ViewedAnnouncements.user_id == user_id).all()

    user_views = user_clicks + user_favorites
    if not user_views:
        return []

    viewed_announcement_ids = [view.announcement_id for view in user_views]
    viewed_indices = [announcement_ids.index(ann_id) for ann_id in viewed_announcement_ids]

    # Calculate similarity scores
    scores = np.sum(similarity_matrix[viewed_indices], axis=0)
    score_indices = np.argsort(scores)[::-1]

    recommended_announcement_ids = [
        announcement_ids[idx]
        for idx in score_indices
        if announcement_ids[idx] not in viewed_announcement_ids
    ][:num_recommendations]

    return recommended_announcement_ids


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/recommendations/{user_id}")
async def get_recommendations_endpoint(user_id: int, db: Session = Depends(get_db), num_recommendations: int = 10):
    recommendations = get_recommendations(user_id, db, num_recommendations)
    if not recommendations:
        raise HTTPException(status_code=404, detail="Recommendations not found")
    return {"user_id": user_id, "recommendations": recommendations}


'''@router.get("/testinteractions")
def get_interaction(db: Session = Depends(get_db)):
    inter = db.query(models.ViewedAnnouncements).all()
    return inter'''