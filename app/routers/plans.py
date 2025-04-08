from fastapi import APIRouter, status
from sqlmodel import select

from models import Plan, PlanCreate
from db import SessionDep


router = APIRouter(tags = ['plans'])


@router.post('/plans', response_model=Plan, status_code=status.HTTP_201_CREATED)
async def create_plan(plan_data: PlanCreate, session: SessionDep):
  plan = Plan.model_validate(plan_data.model_dump())
  session.add(plan)
  session.commit()
  session.refresh(plan)
  return plan

@router.get('/plans/{plan_id}', response_model=Plan)
async def read_plan(plan_id: int, session: SessionDep):
  plan_db = session.get(Plan, plan_id)
  if not plan_db:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND, detail="Plan not found"
    )
  return plan_db

@router.get('/plans', response_model=list[Plan])
async def list_plans(session: SessionDep):
  return session.exec(select(Plan)).all()