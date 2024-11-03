from fastapi import APIRouter, HTTPException
from application.objects.loan import Loan
from application.database.loan import LoanRepo
from application.core.db import db_dependency

router = APIRouter()
loan_db = LoanRepo()

@router.post("/loans/", response_model=Loan)
async def create_loan(db: db_dependency, loan: Loan):
    try:
        cur_loan = await loan_db.add_loan(db, loan)
        return cur_loan
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Input Error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.put("/loans/{loan_id}", response_model=Loan)
async def update_loan(db: db_dependency, loan_id: str, loan: Loan):
    try:
        updated_loan = await loan_db.update_loan_by_id(db, loan, loan_id)
        if updated_loan is None:
            raise HTTPException(status_code=404, detail=f"Loan with ID '{loan_id}' not found")
        return updated_loan
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=f"Input Error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/loans/", response_model=list[Loan])
async def get_all_loans(db: db_dependency):
    try:
        return await loan_db.get_loans(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/loans/{company_id}", response_model=list[Loan])
async def get_loans_by_company(db: db_dependency, company_id: str):
    try:
        loans = await loan_db.get_loans_by_company(db, company_id)
        if loans is None:
            raise HTTPException(status_code=404, detail=f"No loans found for company ID '{company_id}'")
        return loans
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
