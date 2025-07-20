"""
Model loader for Vercel deployment
Downloads models from external storage to avoid size limits
"""
import os
import pickle
import joblib
import requests
from pathlib import Path
import tempfile

# Model URLs (you'll need to upload these to a file hosting service)
MODEL_URLS = {
    "model": "https://github.com/RockingAyush04/swiggy-models/raw/main/model.pkl",
    "preprocessor": "https://github.com/RockingAyush04/swiggy-models/raw/main/preprocessor.joblib",
    "stacking_regressor": "https://github.com/RockingAyush04/swiggy-models/raw/main/stacking_regressor.pkl"
}

def download_model(url: str, filename: str) -> str:
    """Download model from URL to temporary directory"""
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    
    # Only download if not already cached
    if not os.path.exists(file_path):
        print(f"Downloading {filename}...")
        response = requests.get(url)
        response.raise_for_status()
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    
    return file_path

def load_models():
    """Load models from external storage"""
    models = {}
    
    try:
        # Download and load main model
        model_path = download_model(MODEL_URLS["model"], "model.pkl")
        with open(model_path, 'rb') as f:
            models["model"] = pickle.load(f)
        
        # Download and load preprocessor
        preprocessor_path = download_model(MODEL_URLS["preprocessor"], "preprocessor.joblib")
        models["preprocessor"] = joblib.load(preprocessor_path)
        
        print("Models loaded successfully from external storage")
        return models
        
    except Exception as e:
        print(f"Error loading models from external storage: {e}")
        # Fallback to local models for development
        try:
            with open("models/model.pkl", "rb") as f:
                models["model"] = pickle.load(f)
            models["preprocessor"] = joblib.load("models/preprocessor.joblib")
            print("Loaded local models as fallback")
            return models
        except Exception as local_error:
            print(f"Error loading local models: {local_error}")
            raise Exception("Could not load models from external storage or local files")

# Lightweight dummy model for testing
class DummyModel:
    def predict(self, X):
        """Return dummy prediction for testing"""
        import numpy as np
        # Return a reasonable delivery time estimate (15-45 minutes)
        return [25.0 + np.random.normal(0, 5)]

def get_dummy_models():
    """Return dummy models for testing when real models can't be loaded"""
    return {
        "model": DummyModel(),
        "preprocessor": None
    }
