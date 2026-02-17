# ASL Fingerspelling Translator

A computer vision web application that recognizes American Sign Language (ASL) fingerspelling letters (A-J) in real-time and displays them as text.

## 📋 Project Overview

**Course:** CSCI 4390 - Senior Project  
**Team Members:**

- Luis Matamoros (ML Lead)
- Juan Abarca (Backend/Integration Lead)
- Gerardo Quintana (Frontend/UI Lead)
- Kenneth Arevalo (Testing/Documentation Lead)

**Faculty Adviser:** Jonathan Reyes

**Timeline:** Feb 16 - May 14, 2025

## 🎯 Goals

- Recognize 10 ASL letters (A-J) with 70%+ accuracy
- Real-time hand landmark detection using webcam
- Web-based interface accessible via browser
- Manual word separation for letter sequences

## 🛠️ Tech Stack

- **Computer Vision:** MediaPipe Hands
- **Machine Learning:** TensorFlow/Keras, scikit-learn
- **Backend:** Flask
- **Frontend:** Vanilla JavaScript, HTML/CSS
- **Data:** CSV (hand landmark coordinates)

## 📦 Installation

### Prerequisites

- Python 3.8+
- Webcam
- Git

### Setup

1. **Clone the repository**

```bash
   git clone https://github.com/[YOUR-USERNAME]/asl-translator.git
   cd asl-fingerspelling-translator
```

2. **Set up git commit template** (one-time, inside /asl-translator)
```bash
   git config commit.template .gitmessage
```

3. **Create virtual environment**

```bash
   python3 -m venv venv
   source venv/bin/activate  # On Mac/Linux
   # venv\Scripts\activate   # On Windows
```

4. **Install dependencies**

```bash
   pip install -r requirements.txt
```

5. **Verify MediaPipe installation**

```bash
   python test_mediapipe.py
```

   You should see a window with your webcam feed and hand skeleton overlay.

## 🚀 Quick Start

### Data Collection

```bash
python src/data_collection/collect_data.py
```

Press A/B/C/... keys to record samples for each letter. Press 'q' to quit.

### Model Training

```bash
python src/model_training/train_model.py
```

### Run Flask Backend

```bash
python src/backend/app.py
```
Server runs on `http://localhost:5000`

### Open Frontend

```bash
open src/frontend/index.html
```

Or navigate to the file in your browser.

## 📁 Project Structure

```txt
asl-fingerspelling-translator/
├── data/
│   ├── raw/              # Raw CSV files from data collection
│   └── processed/        # Cleaned/split datasets
├── models/
│   ├── saved_models/     # Trained model files (.h5, .pkl)
│   └── training_logs/    # Accuracy/loss logs
├── src/
│   ├── data_collection/  # Scripts to collect hand landmarks
│   ├── model_training/   # Training scripts
│   ├── backend/          # Flask server code
│   └── frontend/         # HTML/CSS/JS files
├── tests/                # Test scripts
├── docs/                 # Documentation
├── requirements.txt      # Python dependencies
└── README.md
```

## 🔄 Development Workflow

### Branch Strategy

- `main` - Production-ready code (protected)
- `feature/[name]-[description]` - Individual features

### Creating a Feature Branch

```bash
git checkout main
git pull
git checkout -b feature/luis-data-collection
```

### Making Changes

```bash
# Make your changes in this order
git status # all red
git add .
git status # all green
git commit # template is set up for you to fill out no need for "-m"
git push origin feature/luis-data-collection
```

### Pull Request

1. Go to GitHub repository
2. Click "Pull Requests" → "New Pull Request"
3. Select your feature branch
4. Fill out PR template
5. Request review from teammate
6. After approval, merge to main

# Back to main for next feature
git checkout main
git pull
git checkout -b feature/luis-next-feature

## 📊 Project Phases

### Phase 1: Proof of Concept (Feb 16 - March 2)

- [x] Setup development environment
- [ ] Build data collection script
- [ ] Collect initial dataset (A/B/C)
- [ ] Train first model (3 letters)
- [ ] Basic Flask endpoint
- [ ] Webcam UI

**Deliverable:** 3-letter recognition working end-to-end

### Phase 2: Scale to 10 Letters (March 3-23)

- [ ] Retrain on A-J alphabet
- [ ] Integrate predictions into Flask
- [ ] Real-time prediction pipeline
- [ ] UI polish

**Deliverable:** 10-letter recognition with 60%+ accuracy

### Phase 3: Polish & Integration (March 24-April 13)

- [ ] Edge case handling
- [ ] Latency optimization
- [ ] Professional UI design
- [ ] Comprehensive testing

**Deliverable:** Fully functional web application

### Phase 4: Final Polish (April 14-May 4)

- [ ] Final accuracy improvements
- [ ] Deployment preparation
- [ ] Demo video production
- [ ] User testing (10+ people)

**Deliverable:** Production-ready product

### Phase 5: Presentation (May 5-14)

- [ ] User testing
- [ ] Final presentation prep
- [ ] Demo rehearsal

## 🧪 Testing

Run all tests:
```bash
python -m pytest tests/
```

## 📝 Documentation

See `docs/` folder for:
- Setup guides
- API documentation
- Model training logs
- User testing results

## 🤝 Contributing

All team members follow the same workflow:
1. Create feature branch
2. Make changes
3. Open pull request
4. Get review from teammate
5. Merge to main

## 📄 License
This project is developed for educational purposes as part of CSCI 4390 at UTRGV.

## 🙏 Acknowledgments

- MediaPipe by Google for hand tracking
- TensorFlow/Keras for ML framework
- Dr. Jonathan Reyes for project guidance