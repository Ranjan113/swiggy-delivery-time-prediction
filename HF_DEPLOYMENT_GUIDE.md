# 🚀 Hugging Face Spaces Deployment Guide

## 📁 Files to Upload to Hugging Face Spaces

### Required Files Structure:
```
swiggy-delivery-predictor/
├── README.md                 # Use README_HF.md content
├── hf_app.py                # Main Gradio application
├── requirements.txt         # Use hf_requirements.txt content  
├── models/
│   ├── model.pkl           # Your trained ML model
│   └── preprocessor.joblib # Your preprocessor
└── src/
    └── data/
        └── data_cleaning.py # Your data cleaning functions
```

## 🔧 Step-by-Step Deployment

### 1. Create Hugging Face Account
- Go to https://huggingface.co
- Sign up for a free account
- Verify your email

### 2. Create New Space
- Click "Create new" → "Space"
- Choose a name: `swiggy-delivery-predictor` (or your preference)
- Select "Gradio" as SDK
- Choose "Public" visibility
- Click "Create Space"

### 3. Upload Files

#### Option A: Web Interface
1. Click "Files" tab in your Space
2. Click "Add file" → "Upload files"
3. Upload all files maintaining the folder structure:
   - Upload `hf_app.py` as `app.py` (rename it)
   - Upload `hf_requirements.txt` as `requirements.txt`
   - Upload `README_HF.md` content as `README.md`
   - Create `models/` folder and upload model files
   - Create `src/data/` folder and upload `data_cleaning.py`

#### Option B: Git (Recommended)
```bash
# Clone your space
git clone https://huggingface.co/spaces/YOUR_USERNAME/swiggy-delivery-predictor
cd swiggy-delivery-predictor

# Copy files from your project
cp ../swiggy-delivery-time-prediction/hf_app.py ./app.py
cp ../swiggy-delivery-time-prediction/hf_requirements.txt ./requirements.txt
cp ../swiggy-delivery-time-prediction/README_HF.md ./README.md

# Copy model files
mkdir -p models
cp ../swiggy-delivery-time-prediction/models/model.pkl ./models/
cp ../swiggy-delivery-time-prediction/models/preprocessor.joblib ./models/

# Copy source code
mkdir -p src/data
cp ../swiggy-delivery-time-prediction/src/data/data_cleaning.py ./src/data/

# Commit and push
git add .
git commit -m "Initial deployment of Swiggy delivery predictor"
git push
```

### 4. Configure Space Settings
- Go to "Settings" tab
- Ensure "SDK" is set to "gradio"
- Set "App file" to "app.py"
- Save settings

### 5. Wait for Build
- Your Space will automatically build and deploy
- Check the "Logs" tab for any errors
- Build usually takes 2-5 minutes

### 6. Test Your App
- Once built, your app will be available at:
  `https://huggingface.co/spaces/YOUR_USERNAME/swiggy-delivery-predictor`
- Test all features to ensure everything works

## 🔧 Troubleshooting

### Common Issues:

1. **Import Errors**:
   - Check `requirements.txt` has all dependencies
   - Ensure version compatibility

2. **Model Loading Errors**:
   - Verify model files are uploaded correctly
   - Check file paths in `app.py`

3. **Build Failures**:
   - Check logs for specific error messages
   - Ensure all required files are present

4. **Performance Issues**:
   - Hugging Face Spaces has 16GB RAM limit
   - Consider model compression if needed

## 📊 Expected Performance

- **Build Time**: 2-5 minutes
- **App Load Time**: 10-30 seconds
- **Prediction Time**: 1-3 seconds
- **Concurrent Users**: Up to 100+ (depends on usage)

## 🎯 Next Steps After Deployment

1. **Test thoroughly** with different input combinations
2. **Share the link** with your team and users
3. **Monitor usage** in the Space analytics
4. **Update models** by simply uploading new model files
5. **Add more features** by modifying `app.py`

## 🔗 Your Live App

After deployment, your app will be live at:
`https://huggingface.co/spaces/YOUR_USERNAME/swiggy-delivery-predictor`

Share this link to showcase your ML project! 🚀

## 💡 Pro Tips

- Use **descriptive commit messages** for updates
- **Pin your Space** for easy access
- **Add tags** to make it discoverable
- **Write good documentation** in README
- **Engage with the community** in discussions

---

🎉 **Your advanced ML model is now deployed and accessible worldwide!**
