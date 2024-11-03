from fastapi import APIRouter, HTTPException
from application.core.db import db_dependency
from application.database.company import CompanyRepo
from application.objects.company import Company

router = APIRouter()
company_db = CompanyRepo()

@router.post("/companies/", response_model=Company)
async def create_company(db: db_dependency, company: Company):
    try:
        return await company_db.add_company(db, company)
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Input Error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.put("/companies/{company_id}", response_model=Company)
async def update_company(db: db_dependency, company_id: str, company: Company):
    try:
        updated_company = await company_db.update_company(db, company_id, company)
        if updated_company is None:
            raise HTTPException(status_code=404, detail=f"Company with ID '{company_id}' not found")
        return updated_company
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Input Error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/companies/", response_model=list[Company])
async def read_companies(db: db_dependency):
    try:
        return await company_db.get_companies(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/companies/{company_id}", response_model=Company)
async def read_company(db: db_dependency, company_id: str):
    try:
        company = await company_db.get_company_by_id(db, company_id)
        if company is None:
            raise HTTPException(status_code=404, detail=f"Company with ID '{company_id}' not found")
        return company
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.delete("/companies/{company_id}")
async def delete_company(db: db_dependency, company_id: str):
    try:
        result = await company_db.delete_company(db, company_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Company with ID '{company_id}' not found")
        return {"status": "success", "message": "Company deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
