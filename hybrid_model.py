"""
Hybrid Model Manager for Swiggy Delivery Time Prediction
Automatically switches between lightweight and full ML models based on environment
"""
import os
import pandas as pd
from typing import Dict, Any, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HybridModelManager:
    def __init__(self):
        self.environment = self._detect_environment()
        self.model_type = None
        self.models = {}
        self._initialize_models()
    
    def _detect_environment(self) -> str:
        """Detect the current environment"""
        if os.environ.get('VERCEL'):
            return 'vercel'
        elif os.environ.get('VERCEL_ENV'):
            return 'vercel'
        elif os.path.exists('models/model.pkl'):
            return 'local'
        else:
            return 'lightweight'
    
    def _initialize_models(self):
        """Initialize the appropriate model based on environment"""
        logger.info(f"Initializing models for environment: {self.environment}")
        
        if self.environment == 'local':
            try:
                self._load_full_ml_models()
                self.model_type = 'ml'
                logger.info("✅ Full ML models loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load ML models: {e}")
                self._load_lightweight_model()
                self.model_type = 'lightweight'
        else:
            self._load_lightweight_model()
            self.model_type = 'lightweight'
    
    def _load_full_ml_models(self):
        """Load the full ML models and preprocessing pipeline"""
        import pickle
        import joblib
        from src.data.data_cleaning import (
            change_column_names, data_cleaning, clean_lat_long, 
            calculate_haversine_distance, create_distance_type, 
            drop_columns, columns_to_drop
        )
        
        # Load models
        with open("models/model.pkl", "rb") as f:
            self.models["model"] = pickle.load(f)
        
        try:
            self.models["preprocessor"] = joblib.load("models/preprocessor.joblib")
        except:
            self.models["preprocessor"] = None
        
        # Store cleaning functions
        self.models["cleaning_pipeline"] = {
            "change_column_names": change_column_names,
            "data_cleaning": data_cleaning,
            "clean_lat_long": clean_lat_long,
            "calculate_haversine_distance": calculate_haversine_distance,
            "create_distance_type": create_distance_type,
            "drop_columns": drop_columns,
            "columns_to_drop": columns_to_drop
        }
    
    def _load_lightweight_model(self):
        """Load the lightweight rules-based model"""
        self.models["lightweight"] = True
        logger.info("✅ Lightweight rules-based model initialized")
    
    def _clean_prediction_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply the full ML cleaning pipeline"""
        # Add a dummy time_taken column for the cleaning pipeline
        data_with_dummy_target = data.copy()
        data_with_dummy_target['Time_taken(min)'] = '20(min) '
        
        # Apply the cleaning pipeline
        pipeline = self.models["cleaning_pipeline"]
        cleaned_data = (
            data_with_dummy_target
            .pipe(pipeline["change_column_names"])
            .pipe(pipeline["data_cleaning"])
            .pipe(pipeline["clean_lat_long"])
            .pipe(pipeline["calculate_haversine_distance"])
            .pipe(pipeline["create_distance_type"])
            .pipe(pipeline["drop_columns"], columns=pipeline["columns_to_drop"])
        )
        
        # Remove the dummy target column if it still exists
        if 'time_taken' in cleaned_data.columns:
            cleaned_data = cleaned_data.drop(columns=['time_taken'])
        
        return cleaned_data
    
    def _lightweight_prediction(self, data: Dict[str, Any]) -> float:
        """Lightweight rules-based prediction"""
        try:
            # Extract key features
            age = float(data.get('Delivery_person_Age', 25))
            ratings = float(data.get('Delivery_person_Ratings', 4.0))
            vehicle_condition = int(data.get('Vehicle_condition', 2))
            traffic = data.get('Road_traffic_density', 'Medium').replace('density ', '')
            weather = data.get('Weatherconditions', 'Sunny').replace('conditions ', '')
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
            logger.error(f"Lightweight prediction error: {e}")
            return 25.0
    
    def predict(self, data: Dict[str, Any]) -> Tuple[float, str]:
        """
        Make prediction using the appropriate model
        Returns (prediction, model_info)
        """
        try:
            if self.model_type == 'ml':
                # Use full ML pipeline
                df = pd.DataFrame([data])
                cleaned_data = self._clean_prediction_data(df)
                
                if self.models.get("preprocessor") is not None:
                    preprocessed = self.models["preprocessor"].transform(cleaned_data)
                    prediction = self.models["model"].predict(preprocessed)[0]
                else:
                    prediction = self.models["model"].predict(cleaned_data)[0]
                
                model_info = "🤖 Advanced ML Model (Local)"
                logger.info(f"ML prediction: {prediction}")
                
            else:
                # Use lightweight rules-based model
                prediction = self._lightweight_prediction(data)
                model_info = "⚡ Lightweight Algorithm (Cloud)"
                logger.info(f"Lightweight prediction: {prediction}")
            
            return float(prediction), model_info
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            # Fallback to lightweight
            fallback_prediction = self._lightweight_prediction(data)
            return fallback_prediction, "🔄 Fallback Algorithm"
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model setup"""
        return {
            "environment": self.environment,
            "model_type": self.model_type,
            "available_models": list(self.models.keys()),
            "is_ml_model": self.model_type == 'ml',
            "model_display_name": "🤖 Advanced ML Model" if self.model_type == 'ml' else "⚡ Lightweight Algorithm"
        }

# Global model manager instance
model_manager = HybridModelManager()
