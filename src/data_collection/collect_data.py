"""
collect_data.py
===============
Reads images from data/raw/<letter>/ folders, extracts MediaPipe
hand landmarks (21 points x 3 coords = 63 features), and saves
them to data/raw/landmarks.csv for model training.

Usage:
    python src/data_collection/collect_data.py
"""

import os
import csv
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
MODEL_PATH = os.path.join(BASE_DIR, 'data', 'hand_landmarker.task')
OUTPUT_CSV = os.path.join(RAW_DIR, 'landmarks.csv')

# MediaPipe HandLandmarker setup
options = vision.HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    num_hands=1,
    min_hand_detection_confidence=0.3
)

detector = vision.HandLandmarker.create_from_options(options)

# Build CSV header: x0, y0, z0, x1, y1, z1, ..., x20, y20, z20, label
HEADER = []
for i in range(21):
    HEADER.extend([f'x{i}', f'y{i}', f'z{i}'])
HEADER.append('label')


def extract_landmarks(image_path):
    """Return list of 63 landmark values or None if no hand detected."""
    try:
        img = mp.Image.create_from_file(image_path)
    except Exception:
        return None

    result = detector.detect(img)

    if not result.hand_landmarks:
        return None

    hand = result.hand_landmarks[0]
    row = []
    for lm in hand:
        row.extend([lm.x, lm.y, lm.z])
    return row


def main():
    letters = sorted([
        d for d in os.listdir(RAW_DIR)
        if os.path.isdir(os.path.join(RAW_DIR, d))
    ])

    if not letters:
        print("No letter folders found in data/raw/")
        return

    print(f"Found letter folders: {letters}")

    rows = []
    for letter in letters:
        letter_dir = os.path.join(RAW_DIR, letter)
        images = [f for f in os.listdir(letter_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        success = 0
        skipped = 0

        for img_file in images:
            landmarks = extract_landmarks(os.path.join(letter_dir, img_file))
            if landmarks:
                rows.append(landmarks + [letter])
                success += 1
            else:
                skipped += 1

        print(f"  {letter}: {success} extracted, {skipped} skipped (no hand detected)")

    # Write CSV
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        writer.writerows(rows)

    print(f"\nSaved {len(rows)} samples to {OUTPUT_CSV}")


if __name__ == '__main__':
    main()
