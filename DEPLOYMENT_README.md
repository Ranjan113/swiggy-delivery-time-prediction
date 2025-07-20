# Swiggy Delivery Time Predictor 🚀

A modern AI-powered web application that predicts delivery time for Swiggy orders using machine learning.

## Features

- **AI-Powered Predictions**: Advanced machine learning model for accurate delivery time estimation
- **Modern UI**: Beautiful glassmorphism design with Tailwind CSS
- **Responsive Design**: Works perfectly on all devices
- **Real-time Processing**: Fast prediction results with comprehensive form validation

## Live Demo

🌐 **[Visit Live Application](https://your-app-name.vercel.app)**

## Local Development

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/swiggy-delivery-time-prediction.git
cd swiggy-delivery-time-prediction
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and visit: `http://localhost:8000`

## Deployment on Vercel

### Quick Deploy
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/swiggy-delivery-time-prediction)

### Manual Deployment

1. **Push to GitHub**:
```bash
git add .
git commit -m "Initial deployment"
git push origin main
```

2. **Connect to Vercel**:
   - Visit [vercel.com](https://vercel.com)
   - Sign up/Login with GitHub
   - Click "New Project"
   - Import your repository
   - Vercel will auto-detect it's a Python project

3. **Deploy**:
   - Click "Deploy"
   - Your app will be live in minutes!

## Tech Stack

- **Backend**: FastAPI, Python
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **ML**: scikit-learn, pandas, numpy
- **Deployment**: Vercel
- **Styling**: Glassmorphism effects, Font Awesome icons

## Project Structure

```
swiggy-delivery-time-prediction/
├── app.py              # FastAPI main application
├── api/
│   └── index.py        # Vercel entry point
├── templates/
│   ├── home.html       # Landing page
│   └── form_predict.html # Prediction form
├── static/
│   ├── custom.css      # Custom styles
│   └── script.js       # JavaScript interactions
├── models/
│   ├── model.pkl       # Trained ML model
│   └── preprocessor.joblib # Data preprocessor
├── src/
│   └── data/
│       └── data_cleaning.py # Data processing pipeline
├── vercel.json         # Vercel configuration
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Features Showcase

### 🎨 Modern Design
- Glassmorphism UI effects
- Gradient backgrounds
- Smooth animations
- Responsive layout

### 🤖 AI Predictions
- Advanced machine learning model
- Real-time processing
- Comprehensive input validation
- Accurate delivery time estimation

### 👥 Team Section
- Professional team showcase
- Social media integration
- Contact information

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- **Email**: your.email@example.com
- **LinkedIn**: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- **GitHub**: [Your GitHub](https://github.com/yourusername)

---

Made with ❤️ by [Your Name]
