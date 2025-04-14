import zoneinfo
import time

from typing import Annotated
from datetime import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, FastAPI, HTTPException, Request, status

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

@app.middleware('http')
async def log_request_time(request: Request, call_next):
   start_time = time.time()
   response = await call_next(request)
   process_time = time.time() - start_time
   print(f"Request: {request.url} - completed in: {process_time:.4f} seconds")
   return response

security = HTTPBasic()

@app.get('/')
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if credentials.username == "admin" and credentials.password == "admin":
       return {"message": f"Hello {credentials.username}"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    

@app.get('/time/{iso_code}')
async def get_time(iso_code: str):
  iso = iso_code.upper()
  timezone_str = country_timezones.get(iso)
  tz = zoneinfo.ZoneInfo(timezone_str)
  return {'time': datetime.now(tz)}