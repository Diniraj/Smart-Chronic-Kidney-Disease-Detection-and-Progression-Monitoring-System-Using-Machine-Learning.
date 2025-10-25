# 🩺 Smart CKD Health Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-4.6.0-green.svg)](https://mongodb.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI-powered healthcare platform for Chronic Kidney Disease (CKD) detection, monitoring, and personalized health management using advanced machine learning algorithms with 98% accuracy.

## 🌟 Key Features

### 🤖 AI-Powered Detection
- **98% Accurate CKD Prediction** using Random Forest algorithm
- **SHAP Explainability** for model interpretability and transparency
- **Real-time Health Assessment** with comprehensive parameter analysis
- **Risk Level Classification** (High/Medium/Low) based on confidence scores

### 🍎 Personalized Health Management
- **Stage-based Diet Plans** tailored to CKD stages (1-5)
- **Exercise Recommendations** based on patient condition and age
- **Lifestyle Tips** for optimal health management
- **AI Health Assistant** powered by Gemini AI for 24/7 support

### 👨‍⚕️ Doctor Analytics Dashboard
- **Comprehensive Analytics** with Chart.js visualizations
- **Patient Management** with search, filter, and export capabilities
- **Prediction History** tracking and monitoring
- **Risk Assessment** and stage distribution analysis
- **Bulk Operations** for efficient patient management

### 🤖 AI Health Assistant
- **24/7 AI Chatbot** powered by Gemini AI
- **Multilingual Support** (English + Kannada)
- **Health Query Resolution** and guidance
- **Context-aware Responses** based on patient data

### 📊 Advanced Analytics & Reporting
- **Real-time Dashboards** with interactive charts
- **Model Performance Metrics** and accuracy tracking
- **Patient Progress Monitoring** over time
- **PDF Report Generation** with email delivery
- **Statistical Analysis** and trend identification

### 🎨 Modern UI/UX
- **Responsive Design** for all devices (mobile, tablet, desktop)
- **Light/Dark Mode** toggle
- **Multilingual Interface** (English/Kannada)
- **2025 Modern Design** with smooth animations
- **Accessibility Features** for better user experience

## 🛠️ Technology Stack

### Backend
- **Flask 2.3.3** - Web framework
- **MongoDB 4.6.0** - Database (localhost:27017)
- **PyMongo** - MongoDB driver
- **Flask-Login** - Authentication & session management

### Machine Learning & AI
- **Scikit-learn 1.5.2** - ML algorithms
- **Random Forest** - Primary model (98% accuracy)
- **SHAP 0.45.1** - Model explainability
- **Pandas/NumPy** - Data processing
- **Google Gemini AI** - Conversational AI assistant

### Frontend
- **HTML5/CSS3** - Modern styling
- **JavaScript ES6+** - Interactive functionality
- **Bootstrap 5** - Responsive framework
- **Chart.js** - Data visualization
- **Progressive Web App** features

### Additional Tools
- **ReportLab** - PDF report generation
- **SMTP** - Email notifications
- **Joblib** - Model persistence
- **Pillow** - Image processing

## 📋 Prerequisites

- **Python 3.8+** (recommended: Python 3.11)
- **MongoDB** (localhost:27017 or MongoDB Atlas)
- **Node.js** (for development tools)
- **Git** for version control

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/smart-ckd-health.git
cd smart-ckd-health
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URI=mongodb://localhost:27017/
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

### 5. Set Up MongoDB
```bash
# Install MongoDB locally or use MongoDB Atlas
# For local MongoDB:
mongod

# Or use MongoDB Atlas cloud service
```

### 6. Initialize Database
```bash
python database_setup.py
```

### 7. Train ML Models
```bash
# Run the Jupyter notebook to train models
jupyter notebook CKD_corrected.ipynb
```

### 8. Start the Application
```bash
python app.py
```

### 9. Access the Application
Open your browser and navigate to: `http://localhost:5000`

## 📁 Project Structure

```
smart-ckd-health/
├── app.py                          # Flask main application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .env                           # Environment variables (create this)
├── database_setup.py              # Database setup and sample data
├── recommendations.py              # Diet & exercise recommendation engine
├── report_generator.py            # PDF report generation & email delivery
├── multilingual.py                # Multilingual support (English + Kannada)
├── test_ai_assistant.py           # AI assistant testing
├── CKD_corrected.ipynb            # ML model training & analysis
├── hospital real time.csv         # Original dataset
├── models/                        # Trained ML models
│   ├── ckd_random_forest_model.pkl
│   ├── ckd_scaler.pkl
│   ├── ckd_label_encoder.pkl
│   ├── feature_names.json
│   └── ckd_shap_explainer.pkl
├── templates/                     # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── patient_dashboard.html
│   ├── doctor_dashboard.html
│   └── report_view.html
└── static/                        # Static assets
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## 🎯 Usage Guide

### For Patients
1. **Sign Up** as a patient with your personal information
2. **Enter Health Parameters** (age, blood pressure, lab values, etc.)
3. **Get CKD Prediction** with confidence score and stage
4. **View Personalized Recommendations** (diet, exercise, lifestyle)
5. **Chat with AI Assistant** for health queries and guidance
6. **Download Reports** for medical records and documentation
7. **Track Progress** with health trend analysis

### For Doctors
1. **Sign Up** as a doctor with your credentials
2. **Access Analytics Dashboard** with comprehensive patient statistics
3. **Monitor Patient Progress** over time with trend analysis
4. **View Prediction History** and model performance metrics
5. **Generate Reports** for patients with PDF export
6. **Manage Patients** with search, filter, and bulk operations
7. **Track Model Performance** and accuracy metrics

## 🔧 Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini AI API key | Yes |
| `MONGODB_URI` | MongoDB connection string | Yes |
| `SECRET_KEY` | Flask secret key for sessions | Yes |
| `FLASK_ENV` | Flask environment (development/production) | No |

### MongoDB Collections
- `patients` - Patient information and health data
- `doctors` - Doctor profiles and credentials
- `predictions` - ML model predictions and results
- `reports` - Generated PDF reports
- `recommendations` - Diet and exercise plans
- `analytics` - Dashboard statistics and metrics
- `messages` - Doctor-patient communication
- `activity_log` - User activity tracking

## 📊 Model Performance

| Algorithm | Accuracy | Precision | Recall | F1-Score |
|-----------|----------|-----------|--------|----------|
| **Random Forest** | **98.08%** | **97.5%** | **98.2%** | **97.8%** |
| Gradient Boosting | 97.31% | 96.8% | 97.5% | 97.1% |
| Decision Tree | 97.69% | 97.2% | 97.8% | 97.5% |
| SVM | 94.23% | 93.5% | 94.8% | 94.1% |
| Logistic Regression | 93.08% | 92.5% | 93.6% | 93.0% |

## 🌐 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /signup` - User registration
- `GET /logout` - User logout

### Predictions & Analytics
- `POST /api/predict` - CKD prediction
- `GET /api/analytics` - Dashboard analytics
- `GET /api/patients` - Patient management
- `GET /api/patient/<id>` - Patient details

### AI Assistant
- `POST /api/chat` - AI assistant chat
- `GET /api/supported-languages` - Available languages

### Reports & Communication
- `GET /api/report/<id>` - Generate PDF report
- `POST /api/messages` - Send messages
- `GET /api/messages` - Retrieve messages

## 🔒 Security Features

- **User Authentication** with Flask-Login
- **Password Hashing** with Werkzeug
- **Session Management** for secure access
- **Input Validation** for all forms
- **MongoDB Injection Protection**
- **CORS Configuration** for API security
- **Environment Variable Protection**

## 📱 Mobile Support

- **Responsive Design** for all screen sizes
- **Touch-optimized Interface**
- **Mobile-friendly Navigation**
- **Progressive Web App** capabilities
- **Offline Support** for basic features

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set up MongoDB Atlas or local MongoDB
2. Configure environment variables
3. Install dependencies: `pip install -r requirements.txt`
4. Run database setup: `python database_setup.py`
5. Start the application: `python app.py`

### Docker Deployment (Optional)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guide
- Write comprehensive tests
- Update documentation
- Ensure all tests pass

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Scikit-learn** for machine learning algorithms
- **Google Gemini AI** for conversational AI capabilities
- **Bootstrap** for responsive design framework
- **Chart.js** for data visualization
- **MongoDB** for database management
- **Flask** for web framework
- **ReportLab** for PDF generation

## 📞 Support & Contact

For support and questions:
- **Create an issue** in the repository
- **Contact the development team**
- **Check the documentation** for common solutions

## 🔮 Future Enhancements

- [ ] **Mobile App Development** (React Native/Flutter)
- [ ] **Advanced Analytics** with ML insights
- [ ] **Integration with Wearable Devices**
- [ ] **Telemedicine Features**
- [ ] **Multi-language Support Expansion**
- [ ] **Advanced Reporting Features**
- [ ] **Patient Reminder System**
- [ ] **Doctor-Patient Communication Portal**
- [ ] **Blockchain Integration** for data security
- [ ] **IoT Device Integration**

## 📈 Roadmap

### Phase 1 (Current)
- ✅ Core ML model implementation
- ✅ Basic web interface
- ✅ Patient and doctor dashboards
- ✅ AI assistant integration

### Phase 2 (Next 3 months)
- 🔄 Mobile app development
- 🔄 Advanced analytics
- 🔄 Telemedicine features
- 🔄 Enhanced security

### Phase 3 (6 months)
- 📋 Blockchain integration
- 📋 IoT device support
- 📋 Advanced AI features
- 📋 Global deployment

---

**Built with ❤️ for better healthcare management**

*Empowering healthcare professionals and patients with AI-driven CKD management solutions.*