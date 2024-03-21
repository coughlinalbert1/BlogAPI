'''
ORM functionality to put data into the database
'''
from sqlalchemy.orm.session import Session
from .models import DbUser
from ..schemas import UserBase
from .hash import Hash
from fastapi import HTTPException, status

def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username=request.username, 
        email=request.email, 
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # this will refresh the object and give the user an id (bc it's autogenerated)
    return new_user

def get_all_users(db: Session):
    return db.query(DbUser).all()

def get_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'User with id {id} not found'
        )
    return user

def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'User with username {username} not found'
        )
    return user

def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == id)
    if user.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'User with id {id} not found'
        )
    user.update({
        DbUser.username: request.username, 
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password)
    })
    db.commit()
    return "ok"

def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id)
    if user.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'User with id {id} not found'
        )
    user.delete()
    db.commit()
    return "ok"

