# from fastapi import FastAPI, Request, Form
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# import pandas as pd
# from sklearn.pipeline import Pipeline
# import joblib
# import uvicorn
# from src.data.data_cleaning import perform_data_cleaning  # Adjust based on your structure

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")

# # Load preprocessor & model
# preprocessor = joblib.load("models/preprocessor.joblib")
# model = joblib.load("models/model.joblib")

# # Create pipeline
# model_pipe = Pipeline(steps=[
#     ("preprocessor", preprocessor),
#     ("regressor", model)
# ])

# # Input fields for form
# input_fields = [
#     "ID", "Delivery_person_ID", "Delivery_person_Age", "Delivery_person_Ratings",
#     "Restaurant_latitude", "Restaurant_longitude",
#     "Delivery_location_latitude", "Delivery_location_longitude",
#     "Order_Date", "Time_Orderd", "Time_Order_picked",
#     "Weatherconditions", "Road_traffic_density", "Vehicle_condition",
#     "Type_of_order", "Type_of_vehicle", "multiple_deliveries",
#     "Festival", "City"
# ]

# @app.get("/", response_class=HTMLResponse)
# def read_home(request: Request):
#     return templates.TemplateResponse("home.html", {"request": request})

# @app.get("/form-predict", response_class=HTMLResponse)
# def form_predict(request: Request):
#     return templates.TemplateResponse("form_predict.html", {"request": request, "fields": input_fields})

# @app.post("/predict", response_class=HTMLResponse)
# async def predict(request: Request, **form_data):
#     df = pd.DataFrame([form_data])
#     cleaned = perform_data_cleaning(df)
#     prediction = model_pipe.predict(cleaned)[0]
#     return templates.TemplateResponse("form_predict.html", {
#         "request": request,
#         "fields": input_fields,
#         "prediction": prediction
#     })

# if __name__ == "__main__":
#     uvicorn.run("app:app", port=8000, host="0.0.0.0", reload=True)















# from fastapi import FastAPI, Request, Form
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# import pandas as pd
# from sklearn.pipeline import Pipeline
# import joblib
# import uvicorn
# from src.data.data_cleaning import perform_data_cleaning  # Adjust based on your structure

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")

# # Load preprocessor & model
# preprocessor = joblib.load("models/preprocessor.joblib")
# model = joblib.load("models/model.joblib")

# model_pipe = Pipeline(steps=[
#     ("preprocessor", preprocessor),
#     ("regressor", model)
# ])

# input_fields = [
#     "ID", "Delivery_person_ID", "Delivery_person_Age", "Delivery_person_Ratings",
#     "Restaurant_latitude", "Restaurant_longitude",
#     "Delivery_location_latitude", "Delivery_location_longitude",
#     "Order_Date", "Time_Orderd", "Time_Order_picked",
#     "Weatherconditions", "Road_traffic_density", "Vehicle_condition",
#     "Type_of_order", "Type_of_vehicle", "multiple_deliveries",
#     "Festival", "City"
# ]

# @app.get("/", response_class=HTMLResponse)
# def read_home(request: Request):
#     return templates.TemplateResponse("home.html", {"request": request})

# @app.get("/form-predict", response_class=HTMLResponse)
# def form_predict(request: Request):
#     return templates.TemplateResponse("form_predict.html", {"request": request, "fields": input_fields})

# @app.post("/predict", response_class=HTMLResponse)
# async def predict(
#     request: Request,
#     ID: str = Form(...),
#     Delivery_person_ID: str = Form(...),
#     Delivery_person_Age: int = Form(...),
#     Delivery_person_Ratings: float = Form(...),
#     Restaurant_latitude: float = Form(...),
#     Restaurant_longitude: float = Form(...),
#     Delivery_location_latitude: float = Form(...),
#     Delivery_location_longitude: float = Form(...),
#     Order_Date: str = Form(...),
#     Time_Orderd: str = Form(...),
#     Time_Order_picked: str = Form(...),
#     Weatherconditions: str = Form(...),
#     Road_traffic_density: str = Form(...),
#     Vehicle_condition: int = Form(...),
#     Type_of_order: str = Form(...),
#     Type_of_vehicle: str = Form(...),
#     multiple_deliveries: int = Form(...),
#     Festival: str = Form(...),
#     City: str = Form(...)
# ):
#     data = {
#         "ID": ID,
#         "Delivery_person_ID": Delivery_person_ID,
#         "Delivery_person_Age": Delivery_person_Age,
#         "Delivery_person_Ratings": Delivery_person_Ratings,
#         "Restaurant_latitude": Restaurant_latitude,
#         "Restaurant_longitude": Restaurant_longitude,
#         "Delivery_location_latitude": Delivery_location_latitude,
#         "Delivery_location_longitude": Delivery_location_longitude,
#         "Order_Date": Order_Date,
#         "Time_Orderd": Time_Orderd,
#         "Time_Order_picked": Time_Order_picked,
#         "Weatherconditions": Weatherconditions,
#         "Road_traffic_density": Road_traffic_density,
#         "Vehicle_condition": Vehicle_condition,
#         "Type_of_order": Type_of_order,
#         "Type_of_vehicle": Type_of_vehicle,
#         "multiple_deliveries": multiple_deliveries,
#         "Festival": Festival,
#         "City": City
#     }

#     df = pd.DataFrame([data])
#     cleaned = perform_data_cleaning(df)
#     prediction = model_pipe.predict(cleaned)[0]

#     return templates.TemplateResponse("form_predict.html", {
#         "request": request,
#         "fields": input_fields,
#         "prediction": prediction
#     })

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)














from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import uvicorn
import pickle
import joblib
from src.data.data_cleaning import (
    change_column_names, 
    data_cleaning, 
    clean_lat_long, 
    calculate_haversine_distance, 
    create_distance_type, 
    drop_columns,
    columns_to_drop
)

app = FastAPI(title="Swiggy Delivery Time Predictor", description="AI-powered delivery time prediction")
templates = Jinja2Templates(directory="templates")

# Mount static files (create static directory if needed)
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass  # Static directory might not exist

# Load the model and preprocessor separately
with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

# Try to load the preprocessor
try:
    import joblib
    preprocessor = joblib.load("models/preprocessor.joblib")
    print("Loaded separate preprocessor")
except:
    print("No separate preprocessor found, using model pipeline")
    preprocessor = None
    model_pipe = model

def clean_prediction_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the same cleaning pipeline as the training data
    but without the target variable (time_taken) since we're predicting it
    """
    # Add a dummy time_taken column for the cleaning pipeline
    data_with_dummy_target = data.copy()
    data_with_dummy_target['Time_taken(min)'] = '20(min) '  # Dummy value in correct format
    
    # Apply the cleaning pipeline
    cleaned_data = (
        data_with_dummy_target
        .pipe(change_column_names)
        .pipe(data_cleaning)
        .pipe(clean_lat_long)
        .pipe(calculate_haversine_distance)
        .pipe(create_distance_type)
        .pipe(drop_columns, columns=columns_to_drop)
    )
    
    # Remove the dummy target column if it still exists
    if 'time_taken' in cleaned_data.columns:
        cleaned_data = cleaned_data.drop(columns=['time_taken'])
    
    return cleaned_data

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

    df = pd.DataFrame([data])

    try:
        cleaned = clean_prediction_data(df)
        
        if preprocessor is not None:
            # Use separate preprocessor and model
            preprocessed = preprocessor.transform(cleaned)
            prediction = model.predict(preprocessed)[0]
        else:
            # Use full pipeline
            prediction = model_pipe.predict(cleaned)[0]
            
    except Exception as e:
        return templates.TemplateResponse("form_predict.html", {
            "request": request,
            "fields": input_fields,
            "error": str(e)
        })

    return templates.TemplateResponse("form_predict.html", {
        "request": request,
        "fields": input_fields,
        "prediction": prediction
    })

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
