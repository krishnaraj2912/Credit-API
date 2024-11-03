from sqlalchemy import Column, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from application.core.db import Base

class Credits(Base):
    __tablename__ = "credits"
    
    id = Column(String, primary_key=True)
    company_id = Column(String, ForeignKey("companies.id"), index=True)
    total_credit = Column(Float)
    entry_date = Column(Date)
    
    company = relationship("Company", back_populates="credits")