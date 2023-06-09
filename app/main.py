import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
#from fraud import Fraud
#from fraud import __version__ as model_version
#import numpy as np
import pickle
#import pandas as pd
from pydantic import BaseModel
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing_extensions import Annotated
import secrets
from pathlib import Path
model_version = "0.1.0"
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from crud import create_fraud
from database import SessionLocal, engine
import json
import requests

models.Base.metadata.create_all(bind=engine)

security = HTTPBasic()
app = FastAPI()
BASE_DIR = Path(__file__).resolve(strict=True).parent

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

with open(f"{BASE_DIR}/classifier.pkl","rb") as f:
    classifier = pickle.load(f) 
#pickle_in = open("classifier.pkl","rb")
#classifier = pickle.load(pickle_in)

class Fraud(BaseModel):
    CUSTOMER_ID: float
    TERMINAL_ID: float
    TX_AMOUNT: float
    TX_TIME_SECONDS: float
    TX_TIME_DAYS: float
    TX_DURING_WEEKEND: float
    TX_DURING_NIGHT: float
    CUSTOMER_ID_NB_TX_1DAY_WINDOW: float
    CUSTOMER_ID_AVG_AMOUNT_1DAY_WINDOW: float
    CUSTOMER_ID_NB_TX_7DAY_WINDOW: float
    CUSTOMER_ID_AVG_AMOUNT_7DAY_WINDOW: float
    CUSTOMER_ID_NB_TX_30DAY_WINDOW: float
    CUSTOMER_ID_AVG_AMOUNT_30DAY_WINDOW: float
    TERMINAL_ID_NB_TX_1DAY_WINDOW: float
    TERMINAL_ID_RISK_1DAY_WINDOW: float
    TERMINAL_ID_NB_TX_7DAY_WINDOW: float
    TERMINAL_ID_RISK_7DAY_WINDOW: float
    TERMINAL_ID_NB_TX_30DAY_WINDOW: float
    TERMINAL_ID_RISK_30DAY_WINDOW: float

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"gerry"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"12345"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

#@app.get("/users/me")
#def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
#    return {"username": credentials.username, "password": credentials.password}

@app.get('/')
def index():
    return {"health_check": "ok", "model_version": model_version}

@app.post('/classify')
def predict_fraud(data:Fraud, credentials: HTTPBasicCredentials = Depends(security)):

    data = data.dict()
    CUSTOMER_ID = data['CUSTOMER_ID']
    TERMINAL_ID = data['TERMINAL_ID']
    TX_AMOUNT = data['TX_AMOUNT']
    TX_TIME_SECONDS = data['TX_TIME_SECONDS']
    TX_TIME_DAYS = data['TX_TIME_DAYS']
    TX_DURING_WEEKEND = data['TX_DURING_WEEKEND']
    TX_DURING_NIGHT = data['TX_DURING_NIGHT']
    CUSTOMER_ID_NB_TX_1DAY_WINDOW = data['CUSTOMER_ID_NB_TX_1DAY_WINDOW']
    CUSTOMER_ID_AVG_AMOUNT_1DAY_WINDOW = data['CUSTOMER_ID_AVG_AMOUNT_1DAY_WINDOW']
    CUSTOMER_ID_NB_TX_7DAY_WINDOW = data['CUSTOMER_ID_NB_TX_7DAY_WINDOW']
    CUSTOMER_ID_AVG_AMOUNT_7DAY_WINDOW = data['CUSTOMER_ID_AVG_AMOUNT_7DAY_WINDOW']
    CUSTOMER_ID_NB_TX_30DAY_WINDOW = data['CUSTOMER_ID_NB_TX_30DAY_WINDOW']
    CUSTOMER_ID_AVG_AMOUNT_30DAY_WINDOW = data['CUSTOMER_ID_AVG_AMOUNT_30DAY_WINDOW']
    TERMINAL_ID_NB_TX_1DAY_WINDOW = data['TERMINAL_ID_NB_TX_1DAY_WINDOW']
    TERMINAL_ID_RISK_1DAY_WINDOW = data['TERMINAL_ID_RISK_1DAY_WINDOW']
    TERMINAL_ID_NB_TX_7DAY_WINDOW = data['TERMINAL_ID_NB_TX_7DAY_WINDOW']
    TERMINAL_ID_RISK_7DAY_WINDOW = data['TERMINAL_ID_RISK_7DAY_WINDOW']
    TERMINAL_ID_NB_TX_30DAY_WINDOW = data['TERMINAL_ID_NB_TX_30DAY_WINDOW']
    TERMINAL_ID_RISK_30DAY_WINDOW = data['TERMINAL_ID_RISK_30DAY_WINDOW']
    #print(data)
   
    #return data

    prediction = classifier.predict([[CUSTOMER_ID,TERMINAL_ID,
    TX_AMOUNT,TX_TIME_SECONDS,
    TX_TIME_DAYS,
    TX_DURING_WEEKEND,
    TX_DURING_NIGHT,
    CUSTOMER_ID_NB_TX_1DAY_WINDOW,
    CUSTOMER_ID_AVG_AMOUNT_1DAY_WINDOW,
    CUSTOMER_ID_NB_TX_7DAY_WINDOW,
    CUSTOMER_ID_AVG_AMOUNT_7DAY_WINDOW,
    CUSTOMER_ID_NB_TX_30DAY_WINDOW,
    CUSTOMER_ID_AVG_AMOUNT_30DAY_WINDOW,
    TERMINAL_ID_NB_TX_1DAY_WINDOW,
    TERMINAL_ID_RISK_1DAY_WINDOW,
    TERMINAL_ID_NB_TX_7DAY_WINDOW,
    TERMINAL_ID_RISK_7DAY_WINDOW,
    TERMINAL_ID_NB_TX_30DAY_WINDOW,
    TERMINAL_ID_RISK_30DAY_WINDOW]])

    token= "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIyNTQxMTIwMTY3OTAiLCJpYXQiOjE2ODI1OTAzNjAsImV4cCI6MTY4MjU5MjE2MH0.-nY1qKFUrAo0FosieGUyszIQ-lCQyWwtRbo2eRwW3_8"
    
    if(prediction[0]>0.5):
        prediction="Fraud Detected"
        #create_fraud(db,Fraud)
    else:
        prediction="Legitimate Transaction"
        url = "http://localhost/fraud/app/sendmoney"# Replace with the URL of the API endpoint
        payload = {"senderAccountNumber": CUSTOMER_ID, "receiverAccountNumber": TERMINAL_ID, "transactionAmount": TX_AMOUNT, "pin": "3099"} # Replace with the payload data
        headers = {'Authorization': 'Bearer ' + "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIyNTQxMTIwMTY3OTAiLCJpYXQiOjE2ODI1OTAzNjAsImV4cCI6MTY4MjU5MjE2MH0.-nY1qKFUrAo0FosieGUyszIQ-lCQyWwtRbo2eRwW3_8",'Content-Type':'application/json'}
        response = requests.post(url,headers=headers, data=json.dumps(payload))
        print(response.content) # Replace with the desired response handling

    return {
        'classification': prediction,
        #'pin':("3099"),  
        'senderAccountNumber': CUSTOMER_ID,
        'receiverAccountNumber': TERMINAL_ID,
        'transactionAmount': TX_AMOUNT
    }


#@app.post("/frauds/", response_model=schemas.Fraud)
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

#uvicorn app:app --reload


       