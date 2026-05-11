from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base
import enum

class DealStatus(enum.Enum):
    lead = "lead"
    qualified = "qualified"
    proposal = "proposal"
    won = "won"
    lost = "lost"

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    company = Column(String)
    title = Column(String)
    status     = Column(Enum(DealStatus), default=DealStatus.lead)
    created_at = Column(DateTime, default=datetime.utcnow)
    deals = relationship("Deal", back_populates="contact")

class Deal(Base):
    __tablename__ = "deals"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    value = Column(Float)
    status = Column(Enum(DealStatus), default=DealStatus.lead)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    contact = relationship("Contact", back_populates="deals")

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    type = Column(String)   # call, email, meeting, note
    note = Column(String)
    contact_id = Column(Integer, ForeignKey("contacts.id"))
    deal_id = Column(Integer, ForeignKey("deals.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)