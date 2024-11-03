from fastapi import APIRouter, HTTPException
from application.objects.annual import Annual
from application.database.annual import AnnualRepo
from application.core.db import db_dependency

router = APIRouter()
annual_db = AnnualRepo()

@router.get("/annual/", response_model=list[Annual])
async def get_annual(db: db_dependency):
    try:
        return await annual_db.get_annual(db)
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Input Error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/annual/{company_id}", response_model=list[Annual])
async def get_annual_by_company(db: db_dependency, company_id: str):
    try:
        cur_annual = await annual_db.get_annual_by_company(db, company_id)
        if cur_annual is None:
            raise HTTPException(status_code=404, detail=f"No data found for company ID '{company_id}'")
        return cur_annual
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Input Error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/annual/", response_model=Annual)
async def post_annual(db: db_dependency, annual: Annual):
    try:
        cur_annual = await annual_db.add_annual(db, annual)
        return cur_annual
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Input Error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.put("/annual/{company_id}/{fiscal_year}", response_model=Annual)
async def update_annual(db: db_dependency, company_id: str, fiscal_year: int, annual: Annual):
    try:
        updated_annual = await annual_db.update_annual_by_year_and_company(db, company_id, fiscal_year, annual)
        return updated_annual
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Input Error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")