from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import uvicorn
import os

# Lightweight app for Vercel deployment
app = FastAPI(title="Swiggy Delivery Time Predictor", description="AI-powered delivery time prediction")
templates = Jinja2Templates(directory="templates")

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass

# Lightweight prediction function for demo
def make_prediction(data: dict) -> float:
    """
    Lightweight prediction logic for Vercel deployment
    Uses simplified rules-based approach instead of heavy ML models
    """
    try:
        # Extract key features
        age = float(data.get('Delivery_person_Age', 25))
        ratings = float(data.get('Delivery_person_Ratings', 4.0))
        vehicle_condition = int(data.get('Vehicle_condition', 2))
        traffic = data.get('Road_traffic_density', 'Medium')
        weather = data.get('Weatherconditions', 'Sunny')
        order_type = data.get('Type_of_order', 'Meal')
        vehicle_type = data.get('Type_of_vehicle', 'motorcycle')
        multiple_deliveries = int(data.get('multiple_deliveries', 0))
        
        # Base time (minutes)
        base_time = 20
        
        # Adjust based on traffic
        traffic_multiplier = {
            'Low': 0.8,
            'Medium': 1.0,
            'High': 1.4,
            'Jam': 1.8
        }.get(traffic, 1.0)
        
        # Adjust based on weather
        weather_multiplier = {
            'Sunny': 1.0,
            'Cloudy': 1.1,
            'Windy': 1.2,
            'Fog': 1.3,
            'Sandstorms': 1.5
        }.get(weather, 1.0)
        
        # Adjust based on vehicle condition
        vehicle_multiplier = {
            0: 1.3,  # Poor
            1: 1.1,  # Fair
            2: 1.0,  # Good
            3: 0.9   # Excellent
        }.get(vehicle_condition, 1.0)
        
        # Adjust based on delivery person experience (inverse of age)
        experience_factor = max(0.8, min(1.2, (35 - age) / 20 + 1))
        
        # Adjust based on ratings
        rating_factor = ratings / 5.0
        
        # Adjust for multiple deliveries
        multi_delivery_penalty = multiple_deliveries * 5
        
        # Calculate final time
        predicted_time = (base_time * traffic_multiplier * weather_multiplier * 
                         vehicle_multiplier * experience_factor * rating_factor) + multi_delivery_penalty
        
        # Ensure reasonable bounds (10-60 minutes)
        predicted_time = max(10, min(60, predicted_time))
        
        return round(predicted_time, 1)
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return 25.0  # Default prediction

input_fields = [
    "ID", "Delivery_person_ID", "Delivery_person_Age", "Delivery_person_Ratings",
    "Restaurant_latitude", "Restaurant_longitude",
    "Delivery_location_latitude", "Delivery_location_longitude",
    "Order_Date", "Time_Orderd", "Time_Order_picked",
    "Weatherconditions", "Road_traffic_density", "Vehicle_condition",
    "Type_of_order", "Type_of_vehicle", "multiple_deliveries",
    "Festival", "City"
]

@app.get("/", response_class=HTMLResponse)
def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/form-predict", response_class=HTMLResponse)
def form_predict(request: Request):
    return templates.TemplateResponse("form_predict.html", {"request": request, "fields": input_fields})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    ID: str = Form(...),
    Delivery_person_ID: str = Form(...),
    Delivery_person_Age: int = Form(...),
    Delivery_person_Ratings: float = Form(...),
    Restaurant_latitude: float = Form(...),
    Restaurant_longitude: float = Form(...),
    Delivery_location_latitude: float = Form(...),
    Delivery_location_longitude: float = Form(...),
    Order_Date: str = Form(...),
    Time_Orderd: str = Form(...),
    Time_Order_picked: str = Form(...),
    Weatherconditions: str = Form(...),
    Road_traffic_density: str = Form(...),
    Vehicle_condition: int = Form(...),
    Type_of_order: str = Form(...),
    Type_of_vehicle: str = Form(...),
    multiple_deliveries: int = Form(...),
    Festival: str = Form(...),
    City: str = Form(...)
):
    data = {
        "ID": ID,
        "Delivery_person_ID": Delivery_person_ID,
        "Delivery_person_Age": Delivery_person_Age,
        "Delivery_person_Ratings": Delivery_person_Ratings,
        "Restaurant_latitude": Restaurant_latitude,
        "Restaurant_longitude": Restaurant_longitude,
        "Delivery_location_latitude": Delivery_location_latitude,
        "Delivery_location_longitude": Delivery_location_longitude,
        "Order_Date": Order_Date,
        "Time_Orderd": Time_Orderd,
        "Time_Order_picked": Time_Order_picked,
        "Weatherconditions": Weatherconditions,
        "Road_traffic_density": Road_traffic_density,
        "Vehicle_condition": Vehicle_condition,
        "Type_of_order": Type_of_order,
        "Type_of_vehicle": Type_of_vehicle,
        "multiple_deliveries": multiple_deliveries,
        "Festival": Festival,
        "City": City
    }

    try:
        prediction = make_prediction(data)
    except Exception as e:
        return templates.TemplateResponse("form_predict.html", {
            "request": request,
            "fields": input_fields,
            "error": f"Prediction failed: {str(e)}"
        })

    return templates.TemplateResponse("form_predict.html", {
        "request": request,
        "fields": input_fields,
        "prediction": prediction
    })

# For Vercel deployment - FastAPI app is already ASGI compatible
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app_lite:app", host="0.0.0.0", port=port, reload=False)
