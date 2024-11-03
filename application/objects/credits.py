from pydantic import BaseModel, field_validator
from datetime import date

class Credits(BaseModel):
    id: str
    company_id: str
    total_credit: float
    entry_date: date

    class Config:
        orm_mode = True
        from_attributes = True
    
    @field_validator('company_id')
    def validate_company_id(cls, value):
        if not value or value.strip() == '':
            raise ValueError('Company ID cannot be null or empty.')
        return value