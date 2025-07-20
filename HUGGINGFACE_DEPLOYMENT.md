# Hugging Face Spaces Deployment Guide

## Quick Setup for Hugging Face Spaces

1. Create account at https://huggingface.co
2. Create new Space with Gradio
3. Upload your files structure:

```
swiggy-predictor/
├── app.py              # Gradio app
├── requirements.txt
├── models/
│   ├── model.pkl
│   └── preprocessor.joblib
├── src/
│   └── data/
│       └── data_cleaning.py
└── README.md
```

## Sample Gradio App (app.py):

```python
import gradio as gr
import pandas as pd
import pickle
import joblib
from src.data.data_cleaning import clean_prediction_data

# Load models
with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)
preprocessor = joblib.load("models/preprocessor.joblib")

def predict_delivery_time(age, ratings, vehicle_condition, traffic, weather, 
                         restaurant_lat, restaurant_lon, delivery_lat, delivery_lon,
                         order_type, vehicle_type, multiple_deliveries, festival, city):
    
    data = {
        "Delivery_person_Age": age,
        "Delivery_person_Ratings": ratings,
        "Vehicle_condition": vehicle_condition,
        "Road_traffic_density": traffic,
        "Weatherconditions": weather,
        "Restaurant_latitude": restaurant_lat,
        "Restaurant_longitude": restaurant_lon,
        "Delivery_location_latitude": delivery_lat,
        "Delivery_location_longitude": delivery_lon,
        "Type_of_order": order_type,
        "Type_of_vehicle": vehicle_type,
        "multiple_deliveries": multiple_deliveries,
        "Festival": festival,
        "City": city,
        # Add other required fields with defaults
        "ID": "demo",
        "Delivery_person_ID": "DEMO001",
        "Order_Date": "01-01-2024",
        "Time_Orderd": "12:00:00",
        "Time_Order_picked": "12:15:00"
    }
    
    df = pd.DataFrame([data])
    cleaned = clean_prediction_data(df)
    preprocessed = preprocessor.transform(cleaned)
    prediction = model.predict(preprocessed)[0]
    
    return f"🕒 Estimated Delivery Time: {prediction:.1f} minutes"

# Create Gradio interface
demo = gr.Interface(
    fn=predict_delivery_time,
    inputs=[
        gr.Number(label="Delivery Person Age", value=30),
        gr.Number(label="Delivery Person Rating", value=4.5, minimum=1, maximum=5),
        gr.Slider(0, 3, label="Vehicle Condition", value=2),
        gr.Dropdown(["Low", "Medium", "High", "Jam"], label="Traffic Density", value="Medium"),
        gr.Dropdown(["Sunny", "Cloudy", "Windy", "Fog", "Sandstorms"], label="Weather", value="Sunny"),
        gr.Number(label="Restaurant Latitude", value=22.745049),
        gr.Number(label="Restaurant Longitude", value=75.892471),
        gr.Number(label="Delivery Latitude", value=22.765049),
        gr.Number(label="Delivery Longitude", value=75.912471),
        gr.Dropdown(["Meal", "Snack", "Drink", "Buffet"], label="Order Type", value="Meal"),
        gr.Dropdown(["motorcycle", "scooter", "bicycle"], label="Vehicle Type", value="motorcycle"),
        gr.Slider(0, 3, label="Multiple Deliveries", value=0),
        gr.Dropdown(["No", "Yes"], label="Festival Day", value="No"),
        gr.Dropdown(["Urban", "Semi-Urban", "Metropolitan"], label="City Type", value="Urban")
    ],
    outputs=gr.Text(label="Prediction Result"),
    title="🍕 Swiggy Delivery Time Predictor",
    description="AI-powered delivery time prediction using advanced machine learning"
)

if __name__ == "__main__":
    demo.launch()
```

## Requirements.txt for Hugging Face:
```
gradio
pandas
scikit-learn
joblib
numpy
```

## Deployment Steps:
1. Upload all files to your Space
2. Add requirements.txt
3. Space will auto-deploy!
4. Your app will be live at: https://huggingface.co/spaces/YOUR_USERNAME/swiggy-predictor
