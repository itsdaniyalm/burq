from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db import get_db, engine
from models import Base, Contact, Deal, Activity
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Burq CRM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

dist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../dist"))
templates = Jinja2Templates(directory=os.path.join(dist_path, "templates"))

app.mount("/static", StaticFiles(directory=os.path.join(dist_path, "static")), name="static")

# ── API ROUTES ──

@app.get("/api/contacts/")
def list_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).all()

@app.get("/api/contacts/{contact_id}/deals")
def contact_deals(contact_id: int, db: Session = Depends(get_db)):
    return db.query(Deal).filter(Deal.contact_id == contact_id).all()

@app.get("/api/contacts/{contact_id}/activities")
def contact_activities(contact_id: int, db: Session = Depends(get_db)):
    return db.query(Activity).filter(Activity.contact_id == contact_id).all()

@app.get("/api/contacts/{contact_id}")
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    return db.query(Contact).filter(Contact.id == contact_id).first()

@app.get("/api/deals/")
def list_deals(db: Session = Depends(get_db)):
    return db.query(Deal).all()

@app.get("/api/deals/{deal_id}")
def get_deal(deal_id: int, db: Session = Depends(get_db)):
    return db.query(Deal).filter(Deal.id == deal_id).first()

@app.get("/api/activities/")
def list_activities(db: Session = Depends(get_db)):
    return db.query(Activity).all()

@app.get("/api/summary/")
def summary(db: Session = Depends(get_db)):
    total_contacts = db.query(Contact).count()
    total_deals    = db.query(Deal).count()
    total_value    = db.query(Deal).with_entities(
        __import__('sqlalchemy').func.sum(Deal.value)
    ).scalar() or 0
    won_deals = db.query(Deal).filter(Deal.status == "won").count()
    return {
        "total_contacts": total_contacts,
        "total_deals":    total_deals,
        "total_value":    round(total_value, 2),
        "won_deals":      won_deals,
    }

# ── PAGE ROUTES ──

@app.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse(request, "index.html", {"page_title": "Dashboard"})

@app.get("/contacts")
def contacts(request: Request):
    return templates.TemplateResponse(request, "contacts.html", {"page_title": "Contacts"})

@app.get("/deals")
def deals(request: Request):
    return templates.TemplateResponse(request, "deals.html", {"page_title": "Deals"})

@app.get("/settings")
def settings(request: Request):
    return templates.TemplateResponse(request, "settings.html", {"page_title": "Settings"})

@app.get("/contacts/{contact_id}")
def contact_detail(request: Request, contact_id: int):
    return templates.TemplateResponse(request, "contacts_contact_id.html", {"page_title": "Contact"})