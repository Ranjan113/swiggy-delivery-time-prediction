@echo off
echo 🚀 Deploying Swiggy Delivery Time Predictor to Vercel
echo.
echo 📋 Deployment Configuration:
echo    - App: app_vercel.py (Hybrid Model System)
echo    - Requirements: requirements_vercel.txt (Minimal dependencies)
echo    - Models: Excluded from deployment (uses lightweight algorithm)
echo    - Size: Under 50MB limit
echo.

echo 🔧 Checking files...
if exist "app_vercel.py" (
    echo ✅ app_vercel.py found
) else (
    echo ❌ app_vercel.py not found
    pause
    exit /b 1
)

if exist "requirements_vercel.txt" (
    echo ✅ requirements_vercel.txt found
) else (
    echo ❌ requirements_vercel.txt not found
    pause
    exit /b 1
)

if exist "hybrid_model.py" (
    echo ✅ hybrid_model.py found
) else (
    echo ❌ hybrid_model.py not found
    pause
    exit /b 1
)

if exist "templates" (
    echo ✅ templates folder found
) else (
    echo ❌ templates folder not found
    pause
    exit /b 1
)

echo.
echo 📦 What will be deployed:
echo    ✅ FastAPI app with hybrid model system
echo    ✅ Lightweight prediction algorithm
echo    ✅ Templates and static files
echo    ✅ Data cleaning functions (minimal)
echo    ❌ ML models (excluded - too large)
echo    ❌ Heavy dependencies (excluded)
echo.

echo 🎯 Expected behavior:
echo    - Local: Uses full ML model (if models exist)
echo    - Vercel: Uses lightweight algorithm automatically
echo    - Same UI and functionality
echo    - Fast deployment and response times
echo.

echo 🚀 Ready to deploy! Run: vercel --prod
echo 📝 Or visit: https://vercel.com/dashboard
echo.
pause
