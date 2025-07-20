@echo off
echo 🚀 Deploying Swiggy Delivery Time Predictor to Vercel
echo.
echo 📋 Deployment Configuration:
echo    - App: api/index.py (Lightweight Algorithm)
echo    - Requirements: requirements.txt (Minimal dependencies)
echo    - Models: Excluded from deployment (uses lightweight algorithm)
echo    - Size: Under 50MB limit
echo.

echo 🔧 Checking files...
if exist "api\index.py" (
    echo ✅ api/index.py found
) else (
    echo ❌ api/index.py not found
    pause
    exit /b 1
)

if exist "requirements.txt" (
    echo ✅ requirements.txt found
) else (
    echo ❌ requirements.txt not found
    pause
    exit /b 1
)

if exist "templates" (
    echo ✅ templates directory found
) else (
    echo ❌ templates directory not found
    pause
    exit /b 1
)

if exist "vercel.json" (
    echo ✅ vercel.json found
) else (
    echo ❌ vercel.json not found
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
