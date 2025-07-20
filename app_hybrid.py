from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import uvicorn
import os
from hybrid_model import model_manager

# Hybrid FastAPI app - adapts to environment automatically
app = FastAPI(
    title="Swiggy Delivery Time Predictor", 
    description="AI-powered delivery time prediction with hybrid model system"
)
templates = Jinja2Templates(directory="templates")

# Mount static files
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass

# Get model info for display
model_info = model_manager.get_model_info()
print(f"🚀 Starting app with {model_info['model_display_name']} in {model_info['environment']} environment")

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
    return templates.TemplateResponse("home.html", {
        "request": request,
        "model_info": model_info
    })

@app.get("/form-predict", response_class=HTMLResponse)
def form_predict(request: Request):
    return templates.TemplateResponse("form_predict.html", {
        "request": request, 
        "fields": input_fields,
        "model_info": model_info
    })

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
        prediction, model_used = model_manager.predict(data)
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
            "error": f"Prediction failed: {str(e)}",
            "model_info": model_info
        })

@app.get("/api/model-info")
def get_model_info():
    """API endpoint to get current model information"""
    return model_manager.get_model_info()

# For development and deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    reload = model_info['environment'] == 'local'
    uvicorn.run("app_hybrid:app", host="0.0.0.0", port=port, reload=reload)
