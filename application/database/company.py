from application.models.company import Company
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class CompanyRepo:
    async def add_company(self, db: AsyncSession, company: Company):
        try:
            cur_company = Company(**company.model_dump())
            db.add(cur_company)
            await db.commit()
            await db.refresh(cur_company)
            return cur_company
        except Exception as e:
            await db.rollback()
            raise e

    async def update_company(self, db: AsyncSession, company_id: str, company: Company):
        try:
            cur_company = await db.execute(select(Company).filter(Company.id == company_id))
            cur_company = cur_company.scalars().first()
            if cur_company:
                for key, value in company.model_dump().items():
                    setattr(cur_company, key, value)
                await db.commit()
                await db.refresh(cur_company)
            return cur_company
        except Exception as e:
            await db.rollback()
            raise e

    async def get_companies(self, db: AsyncSession):
        try:
            all_companies = await db.execute(select(Company))
            return all_companies.scalars().all()
        except Exception as e:
            raise e

    async def get_company_by_id(self, db: AsyncSession, company_id: str):
        try:
            cur_company = await db.execute(select(Company).filter(Company.id == company_id))
            return cur_company.scalars().first()
        except Exception as e:
            raise e

    async def delete_company(self, db: AsyncSession, company_id: str):
        try:
            cur_company = await db.execute(select(Company).filter(Company.id == company_id))
            cur_company = cur_company.scalars().first()
            if cur_company:
                await db.delete(cur_company)
                await db.commit()
            return cur_company
        except Exception as e:
            await db.rollback()
            raise e