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
import pandas as pd
import uvicorn
import pickle
from src.data.data_cleaning import perform_data_cleaning  # Adjust if necessary

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load the full model pipeline (includes preprocessing inside)
with open("models/model.pkl", "rb") as f:
    model_pipe = pickle.load(f)

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
        cleaned = perform_data_cleaning(df)
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
