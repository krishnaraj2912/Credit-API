from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from application.models.loan import Loan
from application.models.annual import Annual
from datetime import datetime
from application.models.credits import Credits
from uuid import uuid4

class CreditsRepo:
    async def add_credit(self, db: AsyncSession, credit: Credits):
        try:
            cur_credit = Credits(**credit.model_dump())
            db.add(cur_credit)
            await db.commit()
            await db.refresh(cur_credit)
            return cur_credit
        except Exception as e:
            await db.rollback()
            raise e
            
    async def update_credit(self, db: AsyncSession, company_id: str):
        try:
            select_unpaid_loans = select(Loan).filter(Loan.company_id == company_id, Loan.status == "Due")
            unpaid_loans = await db.execute(select_unpaid_loans)
            unpaid_loans = unpaid_loans.scalars().all()
            total_unpaid_loans = 0
            if unpaid_loans:
                total_unpaid_loans = sum(cur_loan.amount for cur_loan in unpaid_loans)

            two_years = datetime.now().year - 2
            select_turnover = select(Annual).filter(Annual.company_id == company_id, Annual.fiscal_year >= two_years)
            turnover = await db.execute(select_turnover)
            turnover = turnover.scalars().all()
            if turnover:
                total_turnover = sum(cur_turnover.turnover for cur_turnover in turnover)

            total_credit = total_turnover - total_unpaid_loans

            if total_credit and turnover:
                cur_cred = Credits(id=str(uuid4()), company_id=company_id, total_credit=total_credit, entry_date=datetime.now().date())
                db.add(cur_cred)
                await db.commit()
                await db.refresh(cur_cred)
                return cur_cred
            return None
        except Exception as e:
            await db.rollback()
            raise e

    async def get_credits(self, db: AsyncSession):
        try:
            all_credits = await db.execute(select(Credits))
            return all_credits.scalars().all()
        except Exception as e:
            raise e

    async def get_credits_by_id(self, db: AsyncSession, company_id: str):
        try:
            select_credit_by_company_id = select(Credits).filter(Credits.company_id == company_id)
            cur_credit = await db.execute(select_credit_by_company_id)
            return cur_credit.scalars().all()
        except Exception as e:
            raise e