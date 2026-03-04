"""
MediaPipe Integration Tests
Verifies that the development environment is correctly set up
for the ASL Fingerspelling Translator project.

Prerequisites:
    1. Virtual environment activated: source venv/bin/activate
    2. Dependencies installed: pip install -r requirements.txt
    3. Model file downloaded:
       curl -o models/hand_landmarker.task \
       https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task

Run tests:
    python -m pytest tests/test_mediapipe_setup.py -v

What these tests check:
    - test_imports: All required packages (cv2, mediapipe, pandas, sklearn, flask) load correctly
    - test_model_file_exists: The hand landmarker model file is in models/
    - test_hands_initialization: MediaPipe HandLandmarker creates without errors
    - test_landmark_processing: HandLandmarker can process an image frame
"""

import unittest
import os
import numpy as np

MODEL_PATH = os.path.join(

    os.path.dirname(__file__), '..', 'models', 'hand_landmarker.task'
)


class TestMediaPipeSetup(unittest.TestCase):

    def test_imports(self):
        """Verify all core packages import without errors."""
        import cv2
        import mediapipe as mp
        import pandas as pd
        import sklearn
        import flask

    def test_model_file_exists(self):
        """Verify the hand landmarker model file is downloaded."""
        self.assertTrue(
            os.path.exists(MODEL_PATH),
            f"Model file not found at {MODEL_PATH}. Run:\n"
            "curl -o models/hand_landmarker.task "
            "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
        )

    def test_hands_initialization(self):
        """Verify HandLandmarker initializes with the model file."""
        import mediapipe as mp

        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=MODEL_PATH),
            num_hands=1,
            min_hand_detection_confidence=0.5
        )
        landmarker = mp.tasks.vision.HandLandmarker.create_from_options(options)
        landmarker.close()

    def test_landmark_processing(self):
        """Verify HandLandmarker can process an image without errors."""
        import mediapipe as mp

        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=MODEL_PATH),
            num_hands=1,
            min_hand_detection_confidence=0.5
        )
        landmarker = mp.tasks.vision.HandLandmarker.create_from_options(options)

        # Create a blank 480x640 RGB image (no hand expected)
        blank_image = np.zeros((480, 640, 3), dtype=np.uint8)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=blank_image)

        # Process should run without errors, even with no hand detected
        results = landmarker.detect(mp_image)

        # No hand in a blank image, so landmarks should be empty
        self.assertEqual(len(results.hand_landmarks), 0)
        landmarker.close()


if __name__ == '__main__':
    unittest.main()