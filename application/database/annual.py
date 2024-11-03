from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from application.models.annual import Annual
from application.database.credits import CreditsRepo

class AnnualRepo:
    def __init__(self):
        self.credits_db = CreditsRepo()
        
    async def add_annual(self, db: AsyncSession, annual: Annual):
        try:
            cur_annual = Annual(**annual.model_dump())
            db.add(cur_annual)
            await db.commit()
            await db.refresh(cur_annual)
            await self.credits_db.update_credit(db, annual.company_id)
            return cur_annual
        except Exception as e:
            await db.rollback()
            raise e

    async def update_annual_by_year_and_company(self, db: AsyncSession, company_id: str, fiscal_year: int, annual: Annual):
        try:
            cur_annual = await db.execute(select(Annual).filter(Annual.company_id == company_id, Annual.fiscal_year == fiscal_year))
            cur_annual = cur_annual.scalars().first()
            if cur_annual:
                for key, value in annual.model_dump().items():
                    setattr(cur_annual, key, value)
                await db.commit()
                await db.refresh(cur_annual)
                await self.credits_db.update_credit(db, company_id)
                return cur_annual
            await self.add_annual(db, annual)
        except Exception as e:
            await db.rollback()
            raise e

    async def get_annual(self, db: AsyncSession):
        try:
            annual_infos = await db.execute(select(Annual))
            return annual_infos.scalars().all()
        except Exception as e:
            raise e

    async def get_annual_by_company(self, db: AsyncSession, company_id: str):
        try:
            cur_annual = await db.execute(select(Annual).filter(Annual.company_id == company_id))
            return cur_annual.scalars().all()
        except Exception as e:
            raise e