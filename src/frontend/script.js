/**
 * ASL Fingerspelling Translator - Frontend Logic
 * ================================================
 * Sprint 2: MediaPipe landmark extraction in browser,
 * POST landmarks to Flask /predict, display real predictions.
 */

import { HandLandmarker, FilesetResolver } from
    'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest';

// === DOM Elements ===
const video = document.getElementById('webcam');
const webcamStatus = document.getElementById('webcam-status');
const predictedLetter = document.getElementById('predicted-letter');
const bufferLetters = document.getElementById('buffer-letters');
const btnSign = document.getElementById('btn-sign');
const btnClear = document.getElementById('btn-clear');
const btnComplete = document.getElementById('btn-complete');
const btnBack = document.getElementById('btn-back');
const completeWord = document.getElementById('complete-word');

const backendStatus = document.getElementById('backend-status');
const confidenceEl = document.getElementById('confidence');
const canvas = document.getElementById('landmark-canvas');
const ctx = canvas.getContext('2d');

// === Config ===
const API_BASE = 'http://localhost:5001';
const PREDICT_INTERVAL_MS = 500; // send prediction every 500ms

// === State ===
let wordBuffer = [];
let handLandmarker = null;
let predictionLoop = null;

// === MediaPipe Setup ===
async function initHandLandmarker() {
    const vision = await FilesetResolver.forVisionTasks(
        'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm'
    );

    handLandmarker = await HandLandmarker.createFromOptions(vision, {
        baseOptions: {
            modelAssetPath: 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task',
            delegate: 'GPU'
        },
        runningMode: 'VIDEO',
        numHands: 1
    });

    console.log('HandLandmarker ready');
}

// === Webcam Setup ===
async function startWebcam() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { width: 640, height: 480 }
        });
        video.srcObject = stream;
        webcamStatus.style.display = 'none';

        // Start prediction loop once video is playing
        video.addEventListener('loadeddata', () => {
            startPredictionLoop();
        });
    } catch (err) {
        webcamStatus.textContent = 'Camera access denied. Please allow camera permissions.';
        console.error('Webcam error:', err);
    }
}

// === Hand Landmark Connections (matches MediaPipe hand topology) ===
const HAND_CONNECTIONS = [
    [0,1],[1,2],[2,3],[3,4],       // thumb
    [0,5],[5,6],[6,7],[7,8],       // index
    [0,9],[9,10],[10,11],[11,12],   // middle
    [0,13],[13,14],[14,15],[15,16], // ring
    [0,17],[17,18],[18,19],[19,20], // pinky
    [5,9],[9,13],[13,17]            // palm
];

// === Draw Landmarks on Canvas ===
function drawLandmarks(landmarks) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (!landmarks || landmarks.length === 0) return;

    const points = landmarks[0];
    const w = canvas.width;
    const h = canvas.height;

    // Draw connections
    ctx.strokeStyle = '#00e676';
    ctx.lineWidth = 2;
    for (const [start, end] of HAND_CONNECTIONS) {
        ctx.beginPath();
        ctx.moveTo(points[start].x * w, points[start].y * h);
        ctx.lineTo(points[end].x * w, points[end].y * h);
        ctx.stroke();
    }

    // Draw points
    for (const point of points) {
        ctx.beginPath();
        ctx.arc(point.x * w, point.y * h, 5, 0, 2 * Math.PI);
        ctx.fillStyle = '#00e676';
        ctx.fill();
        ctx.strokeStyle = '#004d40';
        ctx.lineWidth = 1.5;
        ctx.stroke();
    }
}

// === Prediction Loop ===
function startPredictionLoop() {
    if (predictionLoop) return;

    predictionLoop = setInterval(async () => {
        if (!handLandmarker || video.readyState < 2) return;

        const result = handLandmarker.detectForVideo(video, performance.now());

        // Draw landmarks (or clear canvas if no hand)
        drawLandmarks(result.landmarks);

        if (!result.landmarks || result.landmarks.length === 0) {
            predictedLetter.textContent = '—';
            confidenceEl.textContent = '\u00a0';
            return;
        }

        // Flatten 21 landmarks into 63 values [x0, y0, z0, x1, y1, z1, ...]
        const landmarks = [];
        for (const lm of result.landmarks[0]) {
            landmarks.push(lm.x, lm.y, lm.z);
        }

        // Send to backend
        try {
            const res = await fetch(`${API_BASE}/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ landmarks })
            });

            const data = await res.json();
            if (data.letter) {
                predictedLetter.textContent = data.letter;
                confidenceEl.textContent = `${Math.round(data.confidence * 100)}%`;
            }
        } catch {
            // Backend may be temporarily unavailable, keep trying
        }
    }, PREDICT_INTERVAL_MS);
}

// === UI Update ===
function updateBufferDisplay() {
    bufferLetters.innerHTML = '';

    wordBuffer.forEach(letter => {
        const span = document.createElement('span');
        span.className = 'letter-filled';
        span.textContent = letter;
        bufferLetters.appendChild(span);
    });

    const remaining = Math.max(0, 8 - wordBuffer.length);
    for (let i = 0; i < remaining; i++) {
        const slot = document.createElement('span');
        slot.className = 'letter-slot';
        bufferLetters.appendChild(slot);
    }
}

// === Screen Navigation ===
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screenId).classList.add('active');
}

// === Button Handlers ===

btnSign.addEventListener('click', () => {
    const letter = predictedLetter.textContent.trim();
    if (letter && letter !== '—') {
        wordBuffer.push(letter);
        updateBufferDisplay();
    }
});

btnClear.addEventListener('click', () => {
    if (wordBuffer.length > 0) {
        wordBuffer.pop();
        updateBufferDisplay();
    }
});

btnComplete.addEventListener('click', () => {
    if (wordBuffer.length > 0) {
        completeWord.textContent = wordBuffer.join('');
        showScreen('complete-screen');
    }
});

btnBack.addEventListener('click', () => {
    wordBuffer = [];
    updateBufferDisplay();
    predictedLetter.textContent = '—';
    showScreen('main-screen');
});

// === Backend Health Check ===
async function checkBackend() {
    try {
        const res = await fetch(`${API_BASE}/`);
        const data = await res.json();
        if (data.status === 'running') {
            backendStatus.textContent = 'Backend: connected';
            backendStatus.className = 'backend-status connected';
        }
    } catch {
        backendStatus.textContent = 'Backend: disconnected';
        backendStatus.className = 'backend-status disconnected';
    }
}

// === Initialize ===
async function init() {
    checkBackend();
    updateBufferDisplay();
    await initHandLandmarker();
    await startWebcam();
}

init();
