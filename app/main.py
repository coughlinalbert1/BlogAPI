from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse, PlainTextResponse
from .router import blog_get, blog_post, user, article, product, file
from .auth import authentication
from .db import models
from .db.database import engine
from .exceptions import StoryException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(file.router)
app.include_router(authentication.router)
app.include_router(product.router)
app.include_router(article.router)
app.include_router(user.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)

@app.get("/")
def index():
    return {"message": "Hello, World"}
@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={"detail": exc.name}
    )

# @app.exception_handler(HTTPException)
# def http_exception_handler(request: Request, exc: HTTPException):
#     return PlainTextResponse(
#         str(exc), 
#         status_code=status.HTTP_400_BAD_REQUEST
#     )

models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/files', StaticFiles(directory='app/files'), name='files')