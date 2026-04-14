"""
Flask-based Web GUI for LSTM Next Word Prediction
Allows users to input text and get predictions in a beautiful web interface
"""

from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import json
import os

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Global variables for model and tokenizer
model = None
tokenizer = None
reverse_word_map = None
max_seq_length = None
vocab_size = None

def load_model_and_tokenizer():
    """Load the trained model and tokenizer"""
    global model, tokenizer, reverse_word_map, max_seq_length, vocab_size
    
    try:
        # Load model
        model = tf.keras.models.load_model('lstm_model.h5')
        print("✓ Model loaded successfully!")
        
        # Load tokenizer
        with open('tokenizer.json', 'r') as f:
            tokenizer_json = f.read()
            tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(tokenizer_json)
        print("✓ Tokenizer loaded successfully!")
        
        # Create reverse mapping
        reverse_word_map = {v: k for k, v in tokenizer.word_index.items()}
        vocab_size = len(tokenizer.word_index) + 1
        
        # Set max sequence length (from training)
        max_seq_length = 14  # As per the Hamlet notebook
        
        print("✓ All resources loaded successfully!")
        return True
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return False

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict next word(s) from input text
    """
    try:
        data = request.json
        input_text = data.get('text', '').strip()
        num_predictions = int(data.get('num_predictions', 1))
        top_k = int(data.get('top_k', 5))
        
        # Validate input
        if not input_text:
            return jsonify({'error': 'Input text cannot be empty'}), 400
        
        if num_predictions < 1 or num_predictions > 20:
            return jsonify({'error': 'Number of predictions must be between 1 and 20'}), 400
        
        if top_k < 1 or top_k > 20:
            return jsonify({'error': 'Top-k must be between 1 and 20'}), 400
        
        # Predict next words
        predictions_list = []
        current_text = input_text
        
        for step in range(num_predictions):
            # Tokenize
            token_text = tokenizer.texts_to_sequences([current_text])[0]
            
            # Pad sequence
            padded_input = pad_sequences([token_text], maxlen=max_seq_length, padding="pre")
            
            # Predict
            output_probs = model.predict(padded_input, verbose=0)[0]
            
            # Get top-k predictions
            top_k_indices = np.argsort(output_probs)[-top_k:][::-1]
            
            step_predictions = []
            predicted_word = None
            
            for idx in top_k_indices:
                if idx in reverse_word_map:
                    word = reverse_word_map[idx]
                    confidence = float(output_probs[idx])
                    step_predictions.append({
                        'word': word,
                        'confidence': f'{confidence:.4f}',
                        'percentage': f'{confidence * 100:.2f}%'
                    })
                    
                    # Get the most likely word for next iteration
                    if predicted_word is None:
                        predicted_word = word
            
            if predicted_word:
                current_text = current_text + " " + predicted_word
                predictions_list.append({
                    'step': step + 1,
                    'predicted_word': predicted_word,
                    'top_predictions': step_predictions,
                    'full_text': current_text
                })
            else:
                break
        
        return jsonify({
            'success': True,
            'input_text': input_text,
            'predictions': predictions_list,
            'final_text': current_text
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'tokenizer_loaded': tokenizer is not None
    })

if __name__ == '__main__':
    print("Loading LSTM model and tokenizer...")
    print("="*60)
    
    if load_model_and_tokenizer():
        print("="*60)
        print("Starting Flask GUI application...")
        print("Open your browser and go to: http://localhost:5000")
        print("="*60)
        app.run(debug=False, host='0.0.0.0', port=5000)
    else:
        print("Failed to load model. Please check the file paths and try again.")
