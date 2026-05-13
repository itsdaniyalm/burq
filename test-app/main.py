from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="dist/static"), name="static")
templates = Jinja2Templates(directory="dist/templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"page_title": "Dashboard"})