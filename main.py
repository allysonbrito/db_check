import os

import uvicorn
from fastapi import FastAPI
from core.config import settings

import oracledb
import json
import oracledb

app = FastAPI()
@app.get('/')
def index():
    return {'data': 'Hello FastAPI!'}


@app.get("/db/{db_name}")
async def check_db(db_name:str):
  print (db_name)
  global us, pw, sql
  sql = "select * from dual"
  us=""
  pw=""
  if db_name == 'ccp':
    us = os.environ['CCP_USER']
    pw = os.environ['CCP_PASS']
  elif db_name == 'trt':
      us = os.environ['TRT_USER']
      pw = os.environ['TRT_PASS']
  print ('us:' + us)
  print ('pw:' + pw)
  try:
    with oracledb.connect(user=us, password=pw, dsn=os.environ['DSN']) as connection:
      with connection.cursor() as cursor:
        cursor.execute(sql)
        print(cursor.fetchall())
        return {"db_status : 1"}

    connection.close()

  except:
    return {"db_status : 0"}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080)