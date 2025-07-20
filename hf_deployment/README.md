---
title: Swiggy Delivery Time Predictor
emoji: 🍕
colorFrom: orange
colorTo: red
sdk: gradio
sdk_version: 4.44.0
app_file: hf_app.py
pinned: false
license: mit
---

# 🍕 Swiggy Delivery Time Predictor

An AI-powered delivery time prediction system using advanced machine learning to estimate food delivery times with high accuracy.

## 🚀 Features

- **Advanced ML Model**: Stacking Regressor with comprehensive feature engineering
- **Geospatial Intelligence**: Haversine distance calculations for accurate route estimation
- **Weather Analysis**: Multi-factor weather impact modeling
- **Real-time Factors**: Traffic density, vehicle condition, and order complexity analysis
- **Performance Metrics**: Delivery person rating integration

## 🎯 Model Performance

- **Accuracy**: 94%+ on validation data
- **Training Data**: 45,000+ real delivery records
- **Features**: 15+ engineered features from raw data
- **Algorithm**: Stacking Regressor with feature preprocessing pipeline

## 🔧 Technical Stack

- **ML Framework**: scikit-learn
- **Data Processing**: pandas, numpy
- **UI Framework**: Gradio
- **Model Storage**: joblib, pickle
- **Deployment**: Hugging Face Spaces

## 📊 Model Architecture

1. **Data Preprocessing Pipeline**:
   - Column name standardization
   - Data type cleaning and validation
   - Latitude/longitude cleaning
   - Haversine distance calculation
   - Feature engineering

2. **Feature Engineering**:
   - Geospatial distance metrics
   - Time-based features
   - Categorical encoding
   - Numerical scaling

3. **ML Model**:
   - Stacking Regressor ensemble
   - Multiple base learners
   - Advanced preprocessing
   - Cross-validation optimized

## 🏗️ Usage

1. Enter delivery person details (age, ratings)
2. Specify pickup and delivery coordinates
3. Select current conditions (weather, traffic)
4. Configure vehicle and order details
5. Get instant AI-powered time prediction!

## 👥 Team

- **Ranjan Mittal** - ML Engineer & Data Scientist
- **Ayush Padhy** - Full Stack Developer
- **Varundeep Singh** - Frontend Developer

## 📝 License

MIT License - Feel free to use and modify!

## 🔗 Links

- [GitHub Repository](https://github.com/RockingAyush04/swiggy-delivery-time-prediction)
- [FastAPI Version](https://swiggy-predictor.vercel.app)
- [Documentation](https://github.com/RockingAyush04/swiggy-delivery-time-prediction/blob/main/README.md)

---

Built with ❤️ by Team Swiggy Predictor
