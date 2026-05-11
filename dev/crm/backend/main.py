from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from db import get_db, engine
from models import Base, Contact, Deal, Activity
from typing import Optional

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Burq CRM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONTACTS ---

@app.get("/contacts/")
def list_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).all()

@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    return db.query(Contact).filter(Contact.id == contact_id).first()

# --- DEALS ---

@app.get("/deals/")
def list_deals(db: Session = Depends(get_db)):
    return db.query(Deal).all()

@app.get("/deals/{deal_id}")
def get_deal(deal_id: int, db: Session = Depends(get_db)):
    return db.query(Deal).filter(Deal.id == deal_id).first()

@app.get("/contacts/{contact_id}/deals")
def contact_deals(contact_id: int, db: Session = Depends(get_db)):
    return db.query(Deal).filter(Deal.contact_id == contact_id).all()

# --- ACTIVITIES ---

@app.get("/activities/")
def list_activities(db: Session = Depends(get_db)):
    return db.query(Activity).all()

@app.get("/contacts/{contact_id}/activities")
def contact_activities(contact_id: int, db: Session = Depends(get_db)):
    return db.query(Activity).filter(Activity.contact_id == contact_id).all()

# --- SUMMARY ---

@app.get("/summary/")
def summary(db: Session = Depends(get_db)):
    total_contacts = db.query(Contact).count()
    total_deals = db.query(Deal).count()
    total_value = db.query(Deal).with_entities(
        __import__('sqlalchemy').func.sum(Deal.value)
    ).scalar() or 0
    won_deals = db.query(Deal).filter(Deal.status == "won").count()
    return {
        "total_contacts": total_contacts,
        "total_deals": total_deals,
        "total_value": round(total_value, 2),
        "won_deals": won_deals
    }