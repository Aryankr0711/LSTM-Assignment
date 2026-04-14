# 🎭 LSTM GUI Application - Shakespeare Hamlet Next Word Prediction

## Quick Start Guide

This is a beautiful web-based GUI for the LSTM-based next word prediction model trained on Shakespeare's Hamlet.

### Installation & Setup

1. **Install Flask** (if not already installed):
   ```bash
   pip install flask
   ```

2. **Ensure the trained model files exist:**
   - `lstm_model.h5` - The trained LSTM model
   - `tokenizer.json` - The tokenizer used during training

3. **Run the GUI application:**
   ```bash
   python gui_app.py
   ```

4. **Open in Browser:**
   - Navigate to `http://localhost:5000`
   - You should see the beautiful prediction interface

### Features

✨ **Beautiful Interactive GUI**
- Modern gradient design with smooth animations
- Responsive layout that works on desktop and mobile
- Real-time prediction results

🎯 **Easy to Use**
- Enter any phrase from Hamlet
- Select number of words to predict (1-20)
- Choose top-K candidates to display (1-20)
- Get instant predictions with confidence scores

📊 **Detailed Results**
- Shows each predicted word with confidence percentage
- Displays top alternatives for each prediction step
- Visual confidence bars for easy comparison
- Complete final text after all predictions

### How to Use

1. **Enter Text**: Type a phrase from Hamlet (e.g., "You come most" or "God blesse")
2. **Configure Predictions**:
   - Set how many words to predict
   - Set how many top candidates to show
3. **Click Predict**: Press the 🚀 Predict button
4. **View Results**: See predictions with confidence scores

### Tips

- Use phrases that appear in Hamlet for better predictions
- Try shorter phrases initially (2-3 words)
- Increase top-K to see more alternatives
- Use Ctrl+Enter in the text area for quick prediction

### Files

- `gui_app.py` - Flask backend server
- `templates/index.html` - Web interface with HTML, CSS, and JavaScript

### Troubleshooting

**"Model not found" error:**
- Make sure `lstm_model.h5` and `tokenizer.json` are in the same directory as `gui_app.py`

**"Connection refused" error:**
- Make sure the Flask app is running
- Check if port 5000 is available

**Slow predictions:**
- This is normal for the first prediction (model initialization)
- Subsequent predictions should be faster

### Project Information

- **Project**: LSTM-Based Next Word Prediction (Shakespeare Hamlet)
- **Team**: Siddhant Sahu, Aryan Kumar, Amir Furquani
- **Framework**: TensorFlow/Keras
- **Interface**: Flask + HTML/CSS/JavaScript
- **Model**: LSTM with Embedding and Dense layers
- **Training Data**: Shakespeare's Hamlet (25,732 sequences)

### Contact & Support

For issues or questions, please refer to the main project documentation.

---

**Enjoy predicting Shakespearean text! 🎭✨**
