from sqlalchemy import Integer, String, Date, Column
from application.core.db import Base
from sqlalchemy.orm import relationship

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(String, index=True, primary_key=True, nullable=False)
    name = Column(String, index=True)
    address = Column(String)
    reg_date = Column(Date)
    employees_count = Column(Integer)
    contact_number = Column(String)
    email = Column(String)
    website = Column(String)
    
    annual = relationship("Annual", back_populates="company")
    loans = relationship("Loan", back_populates="company")
    credits = relationship("Credits", back_populates="company")