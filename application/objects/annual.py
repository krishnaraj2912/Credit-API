from pydantic import BaseModel, field_validator
from datetime import date

class Annual(BaseModel):
    id: str
    company_id: str
    turnover: float
    profit: float
    fiscal_year: int
    reported_date: date

    class Config:
        orm_mode = True
        from_attributes = True
    
    @field_validator('company_id')
    def validate_company_id(cls, value):
        if not value or value.strip() == '':
            raise ValueError('Company ID cannot be null or empty.')
        return value