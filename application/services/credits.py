from fastapi import APIRouter, HTTPException
from application.objects.credits import Credits
from application.database.credits import CreditsRepo
from application.core.db import db_dependency

router = APIRouter()
credits_db = CreditsRepo()

@router.post("/credits/", response_model=Credits)
async def add_credit(db: db_dependency, credit: Credits):
    try:
        new_credit = await credits_db.add_credit(db, credit)
        return new_credit
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Input Error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.put("/credits/{company_id}", response_model=Credits)
async def update_credit(db: db_dependency, company_id: str, credit: Credits):
    try:
        updated_credit = await credits_db.update_credit(db, company_id, credit)
        if updated_credit is None:
            raise HTTPException(status_code=404, detail=f"Credit not found for company ID '{company_id}'")
        return updated_credit
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Input Error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/credits", response_model=list[Credits])
async def get_all_credits(db: db_dependency):
    try:
        all_credits = await credits_db.get_credits(db)
        return all_credits
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/credits/{company_id}", response_model=list[Credits])
async def get_credit(db: db_dependency, company_id: str):
    try:
        company_credits = await credits_db.get_credits_by_id(db, company_id)
        if company_credits is None:
            raise HTTPException(status_code=404, detail=f"Credit not found for company ID '{company_id}'")
        return company_credits
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
