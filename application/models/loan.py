import enum
from sqlalchemy import Column, String, Date, Enum, Float, ForeignKey
from sqlalchemy.orm import relationship
from application.core.db import Base
from application.models.company import Company

class Status(enum.Enum): 
    Initiated = "Initiated"
    Due = "Due"
    Paid = "Paid"

class Loan(Base):
    __tablename__ = "loans"
    
    id = Column(String, primary_key=True)
    company_id = Column(String,  ForeignKey("companies.id"), index=True)
    date = Column(Date)
    bank = Column(String)
    status = Column(Enum(Status))
    amount = Column(Float)
    
    company = relationship("Company", back_populates="loans")