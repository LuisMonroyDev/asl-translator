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

### Tagging a Version (Snapshots)

Use Git tags to create named snapshots of your project at important milestones. This lets you bookmark a specific commit so you can always return to it later.

```bash
git tag -a v0.1-scaffold -m "Project scaffolding and initial setup"
```

| Flag | Purpose |
|------|---------|
| `-a` | Creates an **annotated tag**, which stores your name, the date, and a message alongside the tag |
| `-m` | Attaches a **description message** to the tag (similar to a commit message) |

**Useful tag commands:**

```bash
git tag                        # List all tags
git show v0.1-scaffold         # View tag details and the commit it points to
git checkout v0.1-scaffold     # Go back to that exact snapshot
git push origin v0.1-scaffold  # Push a specific tag to remote (disregards branch protection)
git push origin --tags         # Push all tags to remote (disregards branch protection)
```

**Deleting and re-creating a tag** (e.g., to move it to a newer commit):

```bash
git tag -d v0.1-scaffold                # Delete the tag locally
git push origin --delete v0.1-scaffold  # Delete the tag from remote (if already pushed)
git tag -a v0.1-scaffold -m "Updated message"  # Re-create it on the current commit
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

## The Pipeline: How Your App Learns Sign Language
Step 1: collect_data.py — "Looking at flashcards"
Imagine you show a robot a bunch of photos of hands making the letter A, B, or C.

For each photo, the robot (MediaPipe) doesn't see the picture the way we do. Instead, it finds 21 dots on the hand — fingertips, knuckles, wrist — and writes down where each dot is (x, y, z position). That's 63 numbers per photo.

It saves all those numbers in a spreadsheet (landmarks.csv) with a label: "these 63 numbers = letter A", "these 63 numbers = letter B", etc.

The confidence threshold we just changed? That's how picky the robot is about saying "yes, I see a hand." At 0.5, it was saying "I'm not sure that's a hand" for a lot of C images — because the C shape curls the fingers together and looks weird to the robot. At 0.3, we told it "don't be so picky, if you kinda see a hand, go ahead and mark the dots."

Step 2: train_model.py — "Studying for the test"
Now we give that spreadsheet to a Random Forest — think of it as a classroom of 100 tiny decision-makers (trees).

Each tree looks at the 63 numbers and learns simple rules like:

"If the thumb dot is far from the index finger dot, it's probably B"
"If all finger dots are bunched together, it's probably A"
"If the fingers curve inward, it's probably C"
When a new hand comes in, all 100 trees vote on what letter it is. Majority wins.

What We Learned About Less Data
With 70 C images skipped, the model had:

A: ~85 examples
B: ~230 examples
C: only ~116 examples
The model saw way more B's during training, so it got really good at B but not as good at C. It's like studying 230 B flashcards but only 116 C flashcards — you'd be great at B but shaky on C.

By lowering the confidence, we rescued more C samples, giving the model more "flashcards" to study from, which makes its C predictions more accurate.

The tradeoff: some of those rescued images might have slightly less accurate dot placements (the robot was less sure), which could add a little noise — but more data almost always beats slightly cleaner data.

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