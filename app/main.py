import zoneinfo

from datetime import datetime
from fastapi import FastAPI

from db import create_all_table
from .routers import customers, invoices, transactions, plans


app = FastAPI(lifespan=create_all_table)
app.include_router(customers.router)
app.include_router(invoices.router)
app.include_router(transactions.router)
app.include_router(plans.router)

country_timezones = {
  'CO': 'America/Bogota',
  'MX': 'America/Mexico_City',
  'AR': 'America/Argentina/Buenos_Aires',
  'BR': 'America/Sao_Paulo',
  'PE': 'America/Lima',
}


@app.get('/')
async def root():
    return {'message': "Hello World"}

@app.get('/time/{iso_code}')
async def time(iso_code: str):
  iso = iso_code.upper()
  timezone_str = country_timezones.get(iso)
  tz = zoneinfo.ZoneInfo(timezone_str)
  return {'time': datetime.now(tz)}


# add this