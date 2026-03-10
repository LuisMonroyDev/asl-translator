/**
 * ASL Fingerspelling Translator - Frontend Logic
 * ================================================
 * Handles webcam feed, button interactions, word buffer,
 * and screen navigation.
 *
 * Current state (Sprint 1):
 *   - Webcam feed displays live
 *   - Buttons manage the word buffer locally
 *   - Predicted letter is a placeholder (will connect to Flask in Sprint 2)
 *
 * Sprint 2 will add:
 *   - MediaPipe landmark extraction in browser
 *   - POST landmarks to Flask /predict endpoint
 *   - Display real predicted letter from model
 */

// === DOM Elements ===
const video = document.getElementById('webcam');
const webcamStatus = document.getElementById('webcam-status');
const predictedLetter = document.getElementById('predicted-letter');
const bufferLetters = document.getElementById('buffer-letters');
const btnSign = document.getElementById('btn-sign');
const btnClear = document.getElementById('btn-clear');
const btnComplete = document.getElementById('btn-complete');
const btnBack = document.getElementById('btn-back');
const mainScreen = document.getElementById('main-screen');
const completeScreen = document.getElementById('complete-screen');
const completeWord = document.getElementById('complete-word');

const backendStatus = document.getElementById('backend-status');

// === Config ===
const API_BASE = 'http://localhost:5001';

// === State ===
let wordBuffer = [];

// === Webcam Setup ===
async function startWebcam() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { width: 640, height: 480 }
        });
        video.srcObject = stream;
        webcamStatus.style.display = 'none';
    } catch (err) {
        webcamStatus.textContent = 'Camera access denied. Please allow camera permissions.';
        console.error('Webcam error:', err);
    }
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

    // Show empty slots if buffer has room (max 12 visible slots)
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

// SIGN: capture current predicted letter and add to word buffer
btnSign.addEventListener('click', () => {
    const letter = predictedLetter.textContent.trim();

    // Don't add placeholder or empty values
    if (letter && letter !== '—' && letter !== '—') {
        wordBuffer.push(letter);
        updateBufferDisplay();
    }
});

// CLEAR: remove last letter from word buffer
btnClear.addEventListener('click', () => {
    if (wordBuffer.length > 0) {
        wordBuffer.pop();
        updateBufferDisplay();
    }
});

// COMPLETE: show the finished word on its own screen
btnComplete.addEventListener('click', () => {
    if (wordBuffer.length > 0) {
        completeWord.textContent = wordBuffer.join('');
        showScreen('complete-screen');
    }
});

// BACK: return to main screen, reset buffer
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
startWebcam();
updateBufferDisplay();
checkBackend();