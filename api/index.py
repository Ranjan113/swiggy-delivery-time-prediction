"""
Vercel API Entry Point - Lightweight Prediction App
"""
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(title="Swiggy Delivery Time Predictor", description="AI-powered delivery time prediction")

# Setup templates directory
templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
templates = Jinja2Templates(directory=templates_dir)

# Lightweight prediction function for Vercel
def lightweight_prediction(data: dict) -> float:
    """Lightweight rules-based prediction optimized for Vercel"""
    try:
        # Extract key features with defaults
        age = float(data.get('Delivery_person_Age', 25))
        ratings = float(data.get('Delivery_person_Ratings', 4.0))
        vehicle_condition = int(data.get('Vehicle_condition', 2))
        traffic = str(data.get('Road_traffic_density', 'Medium')).replace('density ', '')
        weather = str(data.get('Weatherconditions', 'Sunny')).replace('conditions ', '')
        multiple_deliveries = int(data.get('multiple_deliveries', 0))
        
        # Base time (minutes)
        base_time = 20
        
        # Traffic multiplier
        traffic_multipliers = {
            'Low': 0.8, 'Medium': 1.0, 'High': 1.4, 'Jam': 1.8
        }
        traffic_mult = traffic_multipliers.get(traffic, 1.0)
        
        # Weather multiplier
        weather_multipliers = {
            'Sunny': 1.0, 'Cloudy': 1.1, 'Windy': 1.2, 
            'Fog': 1.3, 'Sandstorms': 1.5, 'Stormy': 1.4
        }
        weather_mult = weather_multipliers.get(weather, 1.0)
        
        # Vehicle condition multiplier
        vehicle_multipliers = {0: 1.3, 1: 1.1, 2: 1.0, 3: 0.9}
        vehicle_mult = vehicle_multipliers.get(vehicle_condition, 1.0)
        
        # Experience factor (age-based)
        experience_factor = max(0.8, min(1.2, (35 - age) / 20 + 1))
        
        # Rating factor
        rating_factor = max(0.8, ratings / 5.0)
        
        # Multiple delivery penalty
        multi_delivery_penalty = multiple_deliveries * 5
        
        # Calculate final prediction
        predicted_time = (base_time * traffic_mult * weather_mult * 
                        vehicle_mult * experience_factor * rating_factor) + multi_delivery_penalty
        
        # Ensure reasonable bounds
        return max(10, min(60, round(predicted_time, 1)))
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return 25.0

# Model info for templates
model_info = {
    "environment": "vercel",
    "model_type": "lightweight",
    "is_ml_model": False,
    "model_display_name": "⚡ Lightweight Algorithm"
}

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
    return templates.TemplateResponse("home.html", {"request": request, "model_info": model_info})

@app.get("/form-predict", response_class=HTMLResponse)
def form_predict(request: Request):
    return templates.TemplateResponse("form_predict.html", {"request": request, "fields": input_fields, "model_info": model_info})

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
    # Prepare data for prediction
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
        # Use lightweight prediction
        prediction = lightweight_prediction(data)
        model_used = "⚡ Lightweight Algorithm (Vercel)"
        
        return templates.TemplateResponse("form_predict.html", {
            "request": request,
            "fields": input_fields,
            "prediction": prediction,
            "model_info": model_info,
            "model_used": model_used
        })
        
    except Exception as e:
        return templates.TemplateResponse("form_predict.html", {
            "request": request,
            "fields": input_fields,
            "error": str(e),
            "model_info": model_info
        })

# API endpoint for programmatic access
@app.post("/api/predict")
async def api_predict(request: Request):
    try:
        data = await request.json()
        prediction = lightweight_prediction(data)
        
        return {
            "prediction": prediction,
            "model_used": "⚡ Lightweight Algorithm (Vercel)",
            "environment": "vercel",
            "model_type": "lightweight"
        }
    except Exception as e:
        return {"error": str(e)}

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": "vercel",
        "model_type": "lightweight",
        "model_info": model_info
    }
