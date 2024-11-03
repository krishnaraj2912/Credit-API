from pydantic import BaseModel, EmailStr, field_validator
from datetime import date

class Company(BaseModel):
    name: str
    id: str
    address: str
    reg_date: date
    employees_count: int
    contact_number: str
    email: EmailStr
    website: str
    
    class Config:
        orm_mode = True
        from_attributes = True
        
    @field_validator('id')
    def validate_company_id(cls, value):
        if not value or value.strip() == '':
            raise ValueError('Company ID cannot be null or empty.')
        return value

    @field_validator('employees_count')
    def validate_employees_count(cls, value):
        if value < 0:
            raise ValueError('Number of employees must be non-negative.')
        return value

    @field_validator('contact_number')
    def validate_contact_number(cls, value):
        if not value.isdigit() or len(value) < 10:
            raise ValueError('Contact number must be a valid number with at least 10 digits.')
        return value