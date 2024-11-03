from sqlalchemy import Column, String, Float, ForeignKey, Integer, Date
from sqlalchemy.orm import relationship
from application.core.db import Base

class Annual(Base):
    __tablename__ = "annual"
    id = Column(String, primary_key=True)
    company_id = Column(String, ForeignKey("companies.id"), index=True)
    turnover = Column(Float)
    profit = Column(Float)
    fiscal_year = Column(Integer)
    reported_date = Column(Date)
    
    company = relationship("Company", back_populates="annual")