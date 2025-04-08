from enum import Enum
from tkinter import ACTIVE
from fastapi import status
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field, Relationship


class StatusEnum(str, Enum):
  ACTIVE = 'active'
  INACTIVE = 'inactive'

class CustomerPlan(SQLModel, table=True):
  id: int = Field(primary_key=True)
  plan_id: int = Field(foreign_key='plan.id')
  customer_id: int = Field(foreign_key='customer.id')
  status: StatusEnum = Field(default=StatusEnum.ACTIVE)

class PlanBase(SQLModel):
  name: str = Field(default=None)
  price: int = Field(default=None)
  description: str = Field(default=None)

class PlanCreate(PlanBase):
  pass

class Plan(PlanBase, table=True):
  id: int | None = Field(default=None, primary_key=True)
  customers: list['Customer'] = Relationship(
    back_populates='plans', link_model=CustomerPlan
  )

class CustomerBase(SQLModel):
  name: str = Field(default=None)
  description: str | None = Field(default=None)
  email: EmailStr = Field(default=None, unique=True)
  age: int = Field(default=None)

class CustomerCreate(CustomerBase):
  pass

class CustomerUpdate(CustomerBase):
  pass

class Customer(CustomerBase, table=True):
  id: int | None = Field(default=None, primary_key=True)
  transactions: list['Transaction'] = Relationship(back_populates='customer')
  plans: list[Plan] = Relationship(
    back_populates='customers', link_model=CustomerPlan
  )


class TransactionBase(SQLModel):
  ammount: int
  description: str

class Transaction(TransactionBase, table=True):
  id: int | None = Field(default=None, primary_key=True)
  customer_id: int = Field(foreign_key='customer.id')
  customer: Customer = Relationship(back_populates='transactions')

class TransactionCreate(TransactionBase):
  customer_id: int = Field(foreign_key='customer.id')


class Invoice(BaseModel):
  id: int
  customer_id: Customer
  transactions: list[Transaction]
  total: int

  @property
  def ammount_total(self):
    return sum(transaction.ammount for transaction in self.transactions)