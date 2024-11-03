from application.models.loan import Loan
from application.database.credits import CreditsRepo
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class LoanRepo:
    def __init__(self):
        self.credits_db = CreditsRepo()
        
    async def add_loan(self, db: AsyncSession, loan: Loan):
        try:
            cur_loan = Loan(**loan.model_dump())
            db.add(cur_loan)
            await db.commit()
            await db.refresh(cur_loan)
            await self.credits_db.update_credit(db, cur_loan.company_id)
            return cur_loan
        except Exception as e:
            await db.rollback()
            raise e

    async def update_loan_by_id(self, db: AsyncSession, loan: Loan, loan_id: str):
        try:
            select_loan_by_id = select(Loan).filter(Loan.id == loan_id)
            cur_loan = await db.execute(select_loan_by_id)
            cur_loan = cur_loan.scalars().one_or_none()
            if cur_loan:
                loan_dict = loan.model_dump()
                for key, value in loan_dict.items():
                    setattr(cur_loan, key, value)
                await db.commit()
                await db.refresh(cur_loan)
                await self.credits_db.update_credit(db, cur_loan.company_id)
            return cur_loan
        except Exception as e:
            await db.rollback()
            raise e

    async def get_loans(self, db: AsyncSession):
        try:
            all_loans = await db.execute(select(Loan))
            return all_loans.scalars().all()
        except Exception as e:
            raise e

    async def get_loans_by_company(self, db: AsyncSession, company_id: str):
        try:
            all_loans = await db.execute(select(Loan).filter(Loan.company_id == company_id))
            return all_loans.scalars().all()
        except Exception as e:
            raise e