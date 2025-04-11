from sqlmodel import Session

from db import engine
from models import Transaction, Customer


session = Session(engine)
customer = Customer(
  name = 'Jhofran',
  description = 'Customer Jhofran',
  email = 'jhofran2@email.com',
  age = 28
)
session.add(customer)
session.commit()

for x in range(100):
  session.add(Transaction(
    customer_id = customer.id,
    description = f'Transaction {x}',
    ammount = 10 * x
  ))

session.commit()