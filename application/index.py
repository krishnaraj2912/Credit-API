from fastapi import FastAPI
from application.core.setting import settings
from application.models import annual, company, loan, credits
from application.services import annual as annual_router, company as company_router, loan as loan_router, credits as credit_router
from application.core.db import engine
from contextlib import asynccontextmanager
import uvicorn

async def create_tables():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(annual.Base.metadata.create_all)
            await conn.run_sync(company.Base.metadata.create_all)
            await conn.run_sync(loan.Base.metadata.create_all)
            await conn.run_sync(credits.Base.metadata.create_all)
        except Exception as e:
            raise f"Error while creating table {e}"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

def include_routers(app):
    app.include_router(company_router.router, tags=["companies"])
    app.include_router(annual_router.router, tags=["annual_info"])
    app.include_router(loan_router.router, tags=["loans"])
    app.include_router(credit_router.router, tags=["credits"])


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    docs_url="/service/docs",
)
@app.get("/")
async def main():
    return {"Welcome"}

include_routers(app)
    
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)