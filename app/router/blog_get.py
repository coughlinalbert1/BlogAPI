from fastapi import APIRouter, status, Response, Depends
from .blog_post import required_functionality
from enum import Enum
from typing import Optional

router = APIRouter(
    prefix="/blog",
    tags=["blog"]
)


@router.get(
    '/all',
    summary="Get all blogs",
    description="Simulate getting all blogs from the database",
    response_description="List of available blogs"
)
def get_blogs(page: int = 1, page_size: Optional[int] = None, req_parameter: dict = Depends(required_functionality)) -> dict:
    return {'message' : f'All {page_size} blogs returned from page {page}', 'req_parameter': req_parameter}

@router.get('/{blog_id}/comments/{comment_id}', tags=['comments'])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None, req_parameter: dict = Depends(required_functionality)) -> dict:
    """
    Retrieve a comment by its ID.

    Args:
        id (int): The ID of the blog.
        comment_id (int): The ID of the comment.
        valid (bool, optional): Whether the comment is valid or not. Defaults to True.
        username (str, optional): The username associated with the comment. Defaults to None.

    Returns:
        dict: A dictionary containing the comment details.
    """
    return {'message': f'blog_id: {id}, comment_id: {comment_id}, valid: {valid}, username: {username}'}

class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@router.get('/type/{type}')
def get_blog_type(type: BlogType, req_parameter: dict = Depends(required_functionality)) -> dict:
    return {'message': f'Blog type: {type}'}

@router.get('/{id}', status_code=status.HTTP_200_OK)
def get_blog(id: int, response: Response, req_parameter: dict = Depends(required_functionality)) -> dict:
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': f'Blog with id {id} not found'}
    else:
        response.status_code = status.HTTP_200_OK
        return {'message': f'Blog with id {id}'}