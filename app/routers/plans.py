from fastapi import APIRouter
from sqlalchemy import select

from models import Plan
from db import SessionDep


router = APIRouter(tags = ['plans'])


@router.post('/plans')
async def create_plan(plan_data: Plan, session: SessionDep):
  plan_db = Plan.model_validate(plan_data.model_dump())
  session.add(plan_db)
  session.commit()
  session.refresh(plan_db)
  return plan_data

@router.get('/plans', response_model=list[Plan])
async def list_plans(session: SessionDep):
  plans = session.exec(select(Plan)).all()
  return plans