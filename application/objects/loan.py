from pydantic import BaseModel, field_validator
from datetime import date
from enum import Enum

class Status(str, Enum):
    Initiated = "Initiated"
    Due = "Due"
    Paid = "Paid"

class Loan(BaseModel):
    id: str
    company_id: str
    date: date
    bank: str
    status: Status
    amount: float

    class Config:
        orm_mode = True
        from_attributes = True
    
    @field_validator('company_id')
    def validate_company_id(cls, value):
        if not value or value.strip() == '':
            raise ValueError('Company ID cannot be null or empty.')
        return value