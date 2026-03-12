"""
train_model.py
==============
Loads landmarks.csv, trains a Random Forest classifier, and saves
the model to data/processed/asl_model.pkl.

Usage:
    python src/model_training/train_model.py
"""

import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'landmarks.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'asl_model.pkl')


def main():
    # Load data
    df = pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df)} samples")
    print(f"Class distribution:\n{df['label'].value_counts().to_string()}\n")

    X = df.drop('label', axis=1)
    y = df['label']

    # Split 80/20
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train with class_weight='balanced' to handle uneven sample counts
    clf = RandomForestClassifier(
        n_estimators=100,
        class_weight='balanced',
        random_state=42
    )
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    print("Test Results:")
    print(classification_report(y_test, y_pred))

    accuracy = clf.score(X_test, y_test)
    print(f"Accuracy: {accuracy:.1%}")

    # Save model
    joblib.dump(clf, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == '__main__':
    main()
