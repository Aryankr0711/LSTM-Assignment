from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import json
import re
import os
from typing import List

# Initialize FastAPI application
app = FastAPI(
    title="LSTM Next Word Predictor",
    description="API for predicting the next word in a sequence using LSTM",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and tokenizer
model = None
tokenizer = None
reverse_word_map = None
SEQ_LENGTH = 10
VOCAB_SIZE = 5000

# Request/Response models
class PredictionRequest(BaseModel):
    """Request model for prediction endpoint"""
    text: str
    top_k: int = 1

class PredictionResponse(BaseModel):
    """Response model for prediction endpoint"""
    input_text: str
    predictions: List[dict]

def preprocess_text(text: str) -> str:
    """Preprocess input text"""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s.!?,\'\-]', '', text)
    text = ' '.join(text.split())
    return text

@app.on_event("startup")
async def startup_event():
    """Load model and tokenizer on application startup"""
    global model, tokenizer, reverse_word_map
    
    print("\n" + "="*70)
    print("LSTM Next Word Predictor - Backend Server")
    print("="*70)
    print("Loading model and tokenizer...")
    try:
        # Get the directory where the app.py is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, 'lstm_model.h5')
        tokenizer_path = os.path.join(current_dir, 'tokenizer.json')
        
        # Load the trained model
        model = tf.keras.models.load_model(model_path)
        print(f"✓ Model loaded from {model_path}")
        
        # Load tokenizer from JSON
        with open(tokenizer_path, 'r') as f:
            tokenizer_json = json.load(f)
            tokenizer = tokenizer_from_json(json.dumps(tokenizer_json))
        
        # Create reverse mapping
        reverse_word_map = {v: k for k, v in tokenizer.word_index.items()}
        
        print("✓ Tokenizer loaded successfully!")
        print("✓ Model and tokenizer ready for predictions!")
        print("="*70)
        print("🚀 Frontend available at: http://localhost:8000")
        print("="*70 + "\n")
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        raise

@app.get("/")
async def serve_frontend():
    """Serve the frontend HTML"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LSTM Next Word Predictor</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 700px;
                width: 100%;
                padding: 40px;
            }
            
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            
            .header h1 {
                color: #333;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header p {
                color: #666;
                font-size: 1.1em;
            }
            
            .input-section {
                margin-bottom: 25px;
            }
            
            .input-section label {
                display: block;
                margin-bottom: 10px;
                color: #333;
                font-weight: 600;
                font-size: 1.05em;
            }
            
            .input-group {
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
            }
            
            .input-section textarea {
                width: 100%;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 1em;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                resize: vertical;
                min-height: 100px;
                transition: border-color 0.3s;
            }
            
            .input-section textarea:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .select-group {
                display: flex;
                gap: 10px;
                align-items: center;
            }
            
            .select-group label {
                margin: 0;
                font-weight: 600;
                color: #333;
                font-size: 1em;
            }
            
            .select-group select {
                padding: 10px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 1em;
                cursor: pointer;
                background: white;
                transition: border-color 0.3s;
            }
            
            .select-group select:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .button-group {
                display: flex;
                gap: 10px;
                justify-content: center;
            }
            
            .btn {
                padding: 12px 30px;
                border: none;
                border-radius: 8px;
                font-size: 1.05em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .btn-predict {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                flex: 1;
            }
            
            .btn-predict:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            }
            
            .btn-predict:active {
                transform: translateY(0);
            }
            
            .btn-predict.loading {
                opacity: 0.7;
                cursor: not-allowed;
            }
            
            .btn-clear {
                background: #f0f0f0;
                color: #333;
                padding: 12px 20px;
            }
            
            .btn-clear:hover {
                background: #e0e0e0;
            }
            
            .results-section {
                margin-top: 30px;
                display: none;
            }
            
            .results-section.show {
                display: block;
            }
            
            .results-section h2 {
                color: #333;
                margin-bottom: 15px;
                font-size: 1.3em;
            }
            
            .result-item {
                background: #f9f9f9;
                padding: 15px;
                margin-bottom: 12px;
                border-left: 4px solid #667eea;
                border-radius: 5px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transition: all 0.3s;
            }
            
            .result-item:hover {
                background: #f0f0f0;
                transform: translateX(5px);
            }
            
            .result-word {
                font-size: 1.1em;
                font-weight: 600;
                color: #333;
            }
            
            .result-confidence {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .confidence-text {
                color: #666;
                font-weight: 500;
            }
            
            .confidence-bar {
                width: 100px;
                height: 8px;
                background: #e0e0e0;
                border-radius: 4px;
                overflow: hidden;
            }
            
            .confidence-fill {
                height: 100%;
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                transition: width 0.5s ease;
            }
            
            .error {
                background: #ffebee;
                border-left-color: #f44336;
                color: #c62828;
                padding: 15px;
                border-radius: 5px;
                margin-top: 15px;
                display: none;
                border-left: 4px solid #f44336;
            }
            
            .error.show {
                display: block;
            }
            
            .spinner {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-right: 10px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .status {
                text-align: center;
                color: #666;
                font-size: 0.9em;
                margin-top: 15px;
            }
            
            .success {
                color: #4caf50;
            }
            
            @media (max-width: 600px) {
                .container {
                    padding: 20px;
                }
                
                .header h1 {
                    font-size: 1.8em;
                }
                
                .input-group {
                    flex-direction: column;
                }
                
                .select-group {
                    flex-direction: column;
                    align-items: flex-start;
                }
                
                .button-group {
                    flex-direction: column;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔮 LSTM Next Word Predictor</h1>
                <p>Predict the next word with AI</p>
            </div>
            
            <div class="input-section">
                <label for="textInput">Enter your text:</label>
                <textarea id="textInput" placeholder="Type a few words here... e.g., 'the quick brown'"></textarea>
                
                <div class="input-group select-group" style="margin-top: 15px;">
                    <label for="topK">Number of predictions:</label>
                    <select id="topK">
                        <option value="1">Top 1</option>
                        <option value="3" selected>Top 3</option>
                        <option value="5">Top 5</option>
                        <option value="7">Top 7</option>
                        <option value="10">Top 10</option>
                    </select>
                </div>
                
                <div class="button-group">
                    <button class="btn btn-predict" id="predictBtn" onclick="predictNextWord()">
                        Predict Next Word
                    </button>
                    <button class="btn btn-clear" onclick="clearForm()">Clear</button>
                </div>
            </div>
            
            <div class="error" id="errorDiv"></div>
            
            <div class="results-section" id="resultsSection">
                <h2>Top Predictions:</h2>
                <div id="resultsList"></div>
            </div>
            
            <div class="status" id="status"></div>
        </div>
        
        <script>
            const API_URL = window.location.origin;
            
            async function predictNextWord() {
                const textInput = document.getElementById('textInput').value.trim();
                const topK = parseInt(document.getElementById('topK').value);
                const errorDiv = document.getElementById('errorDiv');
                const resultsSection = document.getElementById('resultsSection');
                const resultsList = document.getElementById('resultsList');
                const predictBtn = document.getElementById('predictBtn');
                const statusDiv = document.getElementById('status');
                
                // Clear previous errors and results
                errorDiv.classList.remove('show');
                errorDiv.innerHTML = '';
                resultsSection.classList.remove('show');
                resultsList.innerHTML = '';
                statusDiv.innerHTML = '';
                
                // Validate input
                if (!textInput) {
                    errorDiv.innerHTML = '⚠️ Please enter some text first!';
                    errorDiv.classList.add('show');
                    return;
                }
                
                // Show loading state
                predictBtn.disabled = true;
                predictBtn.classList.add('loading');
                predictBtn.innerHTML = '<span class="spinner"></span>Predicting...';
                statusDiv.innerHTML = '<p>Processing your request...</p>';
                
                try {
                    const response = await fetch(`${API_URL}/predict`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            text: textInput,
                            top_k: topK
                        })
                    });
                    
                    if (!response.ok) {
                        const error = await response.json();
                        throw new Error(error.detail || 'Prediction failed');
                    }
                    
                    const data = await response.json();
                    
                    // Display results
                    displayResults(data.predictions);
                    resultsSection.classList.add('show');
                    statusDiv.innerHTML = '<p class="success">✓ Prediction completed successfully!</p>';
                    
                } catch (error) {
                    errorDiv.innerHTML = `<strong>❌ Error:</strong> ${error.message}`;
                    errorDiv.classList.add('show');
                    statusDiv.innerHTML = '';
                } finally {
                    predictBtn.disabled = false;
                    predictBtn.classList.remove('loading');
                    predictBtn.innerHTML = 'Predict Next Word';
                }
            }
            
            function displayResults(predictions) {
                const resultsList = document.getElementById('resultsList');
                resultsList.innerHTML = '';
                
                predictions.forEach((pred, index) => {
                    const confidence = (pred.confidence * 100).toFixed(2);
                    const barWidth = (pred.confidence * 100);
                    
                    const resultItem = document.createElement('div');
                    resultItem.className = 'result-item';
                    resultItem.innerHTML = `
                        <div>
                            <div class="result-word">${index + 1}. ${pred.word}</div>
                        </div>
                        <div class="result-confidence">
                            <span class="confidence-text">${confidence}%</span>
                            <div class="confidence-bar">
                                <div class="confidence-fill" style="width: ${barWidth}%"></div>
                            </div>
                        </div>
                    `;
                    
                    resultsList.appendChild(resultItem);
                });
            }
            
            function clearForm() {
                document.getElementById('textInput').value = '';
                document.getElementById('resultsSection').classList.remove('show');
                document.getElementById('errorDiv').classList.remove('show');
                document.getElementById('status').innerHTML = '';
                document.getElementById('textInput').focus();
            }
            
            // Allow Ctrl+Enter to predict
            document.getElementById('textInput').addEventListener('keydown', function(event) {
                if (event.key === 'Enter' && event.ctrlKey) {
                    predictNextWord();
                }
            });
            
            // Focus on input when page loads
            window.addEventListener('load', function() {
                document.getElementById('textInput').focus();
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Predict next word(s) given input text"""
    
    # Validate input
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty")
    
    if request.top_k < 1 or request.top_k > 10:
        raise HTTPException(status_code=400, detail="top_k must be between 1 and 10")
    
    try:
        # Preprocess input
        processed_text = preprocess_text(request.text)
        
        # Tokenize
        token_list = tokenizer.texts_to_sequences([processed_text])[0]
        
        # Ensure sequence has correct length
        if len(token_list) > SEQ_LENGTH:
            token_list = token_list[-SEQ_LENGTH:]
        elif len(token_list) < SEQ_LENGTH:
            token_list = [0] * (SEQ_LENGTH - len(token_list)) + token_list
        
        # Get predictions
        input_array = np.array([token_list])
        predictions_array = model.predict(input_array, verbose=0)[0]
        
        # Get top-k predictions
        top_k_indices = np.argsort(predictions_array)[-request.top_k:][::-1]
        
        # Format results
        predictions_list = []
        for idx in top_k_indices:
            if idx in reverse_word_map:
                word = reverse_word_map[idx]
                confidence = float(predictions_array[idx])
                predictions_list.append({
                    "word": word,
                    "confidence": confidence
                })
        
        return PredictionResponse(
            input_text=request.text,
            predictions=predictions_list
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
