@echo off
echo 🚀 Setting up Hugging Face Deployment Files...
echo.

REM Create deployment directory
if not exist "hf_deployment" mkdir hf_deployment
cd hf_deployment

echo 📁 Copying files for Hugging Face deployment...

REM Copy and rename main files
copy "..\hf_app.py" "app.py"
copy "..\hf_requirements.txt" "requirements.txt" 
copy "..\README_HF.md" "README.md"

REM Copy model files
if not exist "models" mkdir models
copy "..\models\model.pkl" "models\"
copy "..\models\preprocessor.joblib" "models\"

REM Copy source code
if not exist "src\data" mkdir src\data
copy "..\src\data\data_cleaning.py" "src\data\"

echo.
echo ✅ Deployment files ready in 'hf_deployment' folder!
echo.
echo 📋 Next steps:
echo 1. Create account at https://huggingface.co
echo 2. Create new Gradio Space
echo 3. Upload all files from 'hf_deployment' folder
echo 4. Wait for build to complete
echo 5. Share your live ML app! 🎉
echo.

pause
