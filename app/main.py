from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


templates = Jinja2Templates(directory="app/templates")
class Post(BaseModel):
    title: str
    content: str
    id: Optional[int] = None


posts: List[Post] = []

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})

@app.get("/posts/create", response_class=HTMLResponse)
async def create_post_form(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request})

@app.post("/posts/create")
async def create_post(request: Request, title: str = Form(...), content: str = Form(...)):
    post_id = len(posts) + 1
    new_post = Post(title=title, content=content, id=post_id)
    posts.append(new_post)
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})

@app.get("/posts/{post_id}", response_class=HTMLResponse)
async def view_post(request: Request, post_id: int):
    for post in posts:
        if post.id == post_id:
            return templates.TemplateResponse("view_post.html", {"request": request, "post": post})
    raise HTTPException(status_code=404, detail="Post not found")

@app.get("/posts/edit/{post_id}", response_class=HTMLResponse)
async def edit_post_form(request: Request, post_id: int):
    for post in posts:
        if post.id == post_id:
            return templates.TemplateResponse("edit_post.html", {"request": request, "post": post})
    raise HTTPException(status_code=404, detail="Post not found")

@app.post("/posts/edit/{post_id}")
async def edit_post(post_id: int, title: str = Form(...), content: str = Form(...)):
    for post in posts:
        if post.id == post_id:
            post.title = title
            post.content = content
            return {"message": "Post updated successfully", "post": post}
    raise HTTPException(status_code=404, detail="Post not found")
