from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal, Annotated
import pickle
import pandas as pd
from dotenv import load_dotenv
import os
import boto3

load_dotenv()

# AWS credentials (optional if using configured profile or IAM role)
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
REGION = 'us-east-1'  # e.g., 'us-east-1'
BUCKET_NAME = 'ml-model-deployement-123'
OBJECT_KEY = 'tips_rf_model.pkl'

# ✅ Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION
)

# ✅ Download the model file into memory
response = s3.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY)
model_bytes = response['Body'].read()

# ✅ Load the model using pickle
model = pickle.loads(model_bytes)
app = FastAPI(title="Tip Prediction API", description="Predicts restaurant tips based on bill, size, and customer info.", version="1.0")

# Input schema with validation and UI hints
class TipRequest(BaseModel):
    total_bill: Annotated[float, Field(...,gt=0, description="Total bill amount in dollars")]
    sex: Annotated[Literal["Male", "Female"], Field(...,description="Customer's gender")]
    smoker: Annotated[Literal["Yes", "No"], Field(...,description="Is the customer a smoker?")]
    day: Annotated[Literal["Thur", "Fri", "Sat", "Sun"], Field(...,description="Day of the week")]
    time: Annotated[Literal["Lunch", "Dinner"], Field(..., description="Time of the meal")]
    size: Annotated[int, Field(..., ge=1, le=20, description="Size of the dining party")]
    
class Nums(BaseModel):
    a: int
    b: int

# Home route
@app.get("/", tags=["Health"])
def home():
    return {"message": "🚀 Tip Prediction API is up and running!"}

@app.get("/info", tags=["Information"])
def info():
    return {"message": "Hello My name is Abhijeet and this is my first model deployment in AWS and CICD Pipeline."}
@app.get("/view", tags=["view of people"])
def view():
    data = {
        "people": [
            {"name": "Abhijeet", "age": 22, "profession": "Data Scientist"},
            {"name": "John", "age": 30, "profession": "Software Engineer"},
            {"name": "Alice", "age": 28, "profession": "Product Manager"},
            {"name": "Rushita", "age": 22, "profession": "UX Designer"},
            {"name": "Aisha", "age": 23, "profession": "DevOps Engineer"}
        ]
    }
    
    return data

@app.post("/add", tags=["Addition"])
def add_two_numbers(nums: Nums):
    return nums.a + nums.b

# Predict route
@app.post("/predict", tags=["Prediction"])
def predict(data: TipRequest):
    input_df = pd.DataFrame([data.dict()])
    prediction = model.predict(input_df)[0]
    return {
        "inputs": data.dict(),
        "predicted_tip": round(prediction, 2)
    }
