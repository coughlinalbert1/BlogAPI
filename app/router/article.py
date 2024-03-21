from fastapi import APIRouter, Depends
from ..schemas import ArticleBase, ArticleDisplay, UserBase
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db import db_article
from typing import List
from ..auth.oauth2 import oauth2_scheme, get_current_user


router = APIRouter(
    prefix='/article',
    tags=['article']
)

# Create article
@router.post('/', response_model=ArticleDisplay, status_code=201)
def article(request: ArticleBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)) -> ArticleDisplay:
    '''
    Create a new article in the database.

    Args:
        request (ArticleBase): The article data to be created.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        Article: The created article.
    '''
    return db_article.create_article(db, request)

# Get specific article
@router.get('/{article_id}')
def single_article(article_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    return {
        'data': db_article.get_article(db, article_id),
        'current_user': current_user
    }