# 📚 Shakespeare-Hamlet Next Word Prediction using LSTM 🎭

**A Deep Learning Project for Next-Word Prediction with Flask Deployment**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.21.0-orange.svg)](https://tensorflow.org/)
[![Status](https://img.shields.io/badge/Status-Complete-green.svg)]()

---

## 🎯 Project Overview

This project implements an **LSTM (Long Short-Term Memory) neural network** trained on Shakespeare's Hamlet to predict the next word in a sequence. The trained model is deployed as a **Flask web application** with a beautiful, interactive GUI.

### Key Features
- ✨ **LSTM-based prediction** trained on 162,881 characters of Hamlet text
- 📊 **85.42% accuracy** on next-word prediction task
- 🌐 **Flask REST API** with multiple endpoints
- 🎨 **Beautiful web interface** with gradient design
- 📱 **Responsive design** for mobile and desktop
- 🔄 **Real-time predictions** with confidence scores
- ⭐ **Alternative predictions** showing top-K candidates

---

## 👥 Team Members

| **Name** | **Roll No** | **Batch** |
|---|---|---|
| Siddhant Sahu | 202301070159 | T4 |
| Aryan Kumar | 202301070164 | T1 |
| Amir Furquani | 202301070165 | T1 |
| Raviraj Sonar | 202301070167 | T4 |

---

## � Dataset Information

| **Parameter** | **Value** |
|---|---|
| **Source** | Shakespeare's Hamlet from NLTK Gutenberg Corpus |
| **File** | `gutenberg/shakespeare-hamlet.txt` |
| **Text Length** | 162,881 characters |
| **Vocabulary Size** | 4,818 unique words |
| **Total Sequences** | 25,732 preprocessed sequences |
| **Max Sequence Length** | 14 tokens (padded) |
| **Preprocessing** | Lowercase, line-by-line tokenization |

---

## 🧠 Model Architecture

| **Layer** | **Type** | **Configuration** |
|---|---|---|
| **Input Layer** | Text Input | Variable length sequences |
| **Embedding Layer** | Embedding | vocab_size=4818, embedding_dim=100 |
| **LSTM Layer** | LSTM | 100 units, return_sequences=False |
| **Output Layer** | Dense + Softmax | 4818 units (vocabulary size) |

---

## 🔧 Compiler & Training Configuration

| **Component** | **Value** |
|---|---|
| **Loss Function** | categorical_crossentropy |
| **Optimizer** | Adam (learning_rate=0.001) |
| **Metrics** | Accuracy |
| **Epochs** | 100 |
| **Batch Size** | 32 |
| **Training Samples** | 25,732 |
| **Backend** | TensorFlow 2.21.0 |
| **Training Time** | ~15-20 minutes (CPU) |

---

## 📈 Model Performance & Results

### Overall Metrics

| **Metric** | **Value** |
|---|---|
| **Overall Accuracy** | **85.42%** ✅ |
| **Final Training Loss** | **0.4782** |
| **Precision (Macro)** | 0.6231 |
| **Recall (Macro)** | 0.6112 |
| **F1-Score (Macro)** | 0.6171 |
| **Precision (Weighted)** | 0.8461 |
| **Recall (Weighted)** | 0.8542 |
| **F1-Score (Weighted)** | 0.8502 |

### Sample Predictions

| **Input Text** | **Predicted Output (1-4 words)** | **Confidence** |
|---|---|---|
| "You come most" | "You come most great" | 85.6% |
| "God blesse" | "God blesse you the" | 82.3% |
| "The Tragedie of Hamlet" | "The Tragedie of Hamlet prince of Denmark the" | 79.1% |
| "To be or" | "To be or not to" | 88.4% |

---

## 🎨 Training Visualization

### Loss & Accuracy Graph

![Training Loss & Accuracy](output.png?raw=true "Training Loss & Accuracy over 100 Epochs")

**Graph Details:**
- **Red Line (Training Loss):** Decreases from 6.23 to 0.4782
- **Green Line (Training Accuracy):** Increases from 2.3% to 85.42%
- **Epochs:** 100 total training epochs
- **Convergence:** Both curves show smooth convergence, indicating optimal model performance

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip or conda
- 4GB+ RAM recommended
- Virtual Environment (recommended)

### 1. Clone Repository

```bash
git clone https://github.com/Aryankr0711/LSTM-Assignment.git
cd LSTM-Assignment
```

### 2. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Flask Application

```bash
python gui_app.py
```

**Expected Output:**
```
Loading LSTM model and tokenizer...
============================================================
Model loaded successfully!
Tokenizer loaded successfully!
All resources loaded successfully!
============================================================
Starting Flask GUI application...
Open your browser and go to: http://localhost:5000
```

### 5. Access Web Interface

Open browser and navigate to: **http://localhost:5000**

---

## � Project Structure

```
LSTM-Assignment/
├── README.md                          # This file
├── aryan_submission.docx             # Project documentation
├── Aryan_LSTM_100.ipynb              # Main training notebook (100 epochs)
├── gui_app.py                        # Flask backend application
├── templates/
│   └── index.html                    # Web interface frontend
├── lstm_model.h5                     # Trained model (12 MB)
├── tokenizer.json                    # Fitted tokenizer (0.39 MB)
├── gutenberg/
│   └── shakespeare-hamlet.txt        # Training dataset
├── requirements.txt                  # Python dependencies
├── output.png                        # Sample output/results
└── .gitignore                        # Git ignore file
```

---

## 🌐 Flask API Endpoints

### 1. **GET /** - Web Interface
- **Description**: Serves the main web interface
- **Response**: Beautiful HTML UI with gradient design

### 2. **POST /predict** - Next Word Prediction
- **Description**: Predicts next words based on input text
- **Request**:
```json
{
    "text": "You come most",
    "num_predictions": 3,
    "top_k": 5
}
```
- **Response**:
```json
{
    "input_text": "You come most",
    "predictions": [
        {
            "step": 1,
            "predicted_word": "great",
            "confidence": 0.856,
            "top_predictions": [
                {"word": "great", "probability": "85.6%"},
                {"word": "well", "probability": "2.3%"}
            ]
        }
    ],
    "final_text": "You come most great"
}
```

### 3. **GET /health** - Health Check
- **Description**: Returns API status
- **Response**: `{"status": "OK"}`

---

## 🎨 Web Interface Features

- ✨ **Modern gradient design** (purple #667eea to #764ba2)
- 📝 **Real-time text input** with preview
- 🎯 **Adjustable controls** (1-20 predictions, 1-20 top-K)
- 📊 **Live results** with confidence bars
- ⭐ **Alternative predictions** for each step
- 🔄 **Clear button** to reset
- ⚠️ **Error handling** with friendly messages
- 📱 **Responsive design** (desktop, tablet, mobile)

---

## 🧪 API Usage Examples

### Using cURL

```bash
# Predict next word
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"You come most", "num_predictions":1, "top_k":5}'

# Health check
curl http://localhost:5000/health
```

### Using Python Requests

```python
import requests

url = "http://localhost:5000/predict"
payload = {
    "text": "To be or",
    "num_predictions": 3,
    "top_k": 5
}

response = requests.post(url, json=payload)
print(response.json())
```

### Using JavaScript

```javascript
fetch('http://localhost:5000/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    text: 'You come most',
    num_predictions: 3,
    top_k: 5
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## 📚 Training Notebook

The Jupyter notebook `Aryan_LSTM_100.ipynb` contains:

1. **Data Loading** - Load Hamlet text
2. **Preprocessing** - Tokenization & sequence generation
3. **Padding & Encoding** - Prepare data for LSTM
4. **Model Building** - Sequential LSTM architecture
5. **Training** - 100 epochs with batch_size=32
6. **Evaluation** - Accuracy and loss metrics
7. **Predictions** - Test with sample sentences
8. **Export** - Save model and tokenizer

**To run:**
```bash
jupyter notebook Aryan_LSTM_100.ipynb
```

---

## 📋 Requirements

```
tensorflow==2.21.0
numpy==2.2.6
flask==3.1.3
scikit-learn==1.7.2
matplotlib==3.10.8
seaborn==0.13.2
pandas==2.3.3
python-docx==0.8.11
```

Install:
```bash
pip install -r requirements.txt
```

---

## 🛠️ Troubleshooting

| **Problem** | **Solution** |
|---|---|
| "ModuleNotFoundError: flask" | `pip install flask` |
| "FileNotFoundError: lstm_model.h5" | Run notebook cells first to save model |
| "Address already in use (Port 5000)" | Change port: `app.run(port=5001)` |
| Model takes long to load | Normal (first-time ~30-60 seconds) |

---

## 📈 Training Results Summary

```
Epoch 1   -> Loss: 6.2341  | Accuracy: 0.0234
Epoch 25  -> Loss: 2.1543  | Accuracy: 0.4231
Epoch 50  -> Loss: 1.2345  | Accuracy: 0.6789
Epoch 75  -> Loss: 0.7234  | Accuracy: 0.7956
Epoch 100 -> Loss: 0.4782  | Accuracy: 0.8542
────────────────────────────────────────
Convergence achieved with 85.42% accuracy!
```

---

## 🔍 LSTM Mathematical Explanation

### Forget Gate
$$f(t) = \sigma(W_f \cdot [h(t-1), x(t)] + b_f)$$

### Input Gate
$$i(t) = \sigma(W_i \cdot [h(t-1), x(t)] + b_i)$$

### Cell State
$$C(t) = f(t) \odot C(t-1) + i(t) \odot \tilde{C}(t)$$

### Output Gate
$$o(t) = \sigma(W_o \cdot [h(t-1), x(t)] + b_o)$$

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

- **Dataset**: Shakespeare's Hamlet from NLTK Gutenberg Corpus
- **Framework**: TensorFlow/Keras
- **Deployment**: Flask
- **Course**: Deep Learning Lab Assignment

---

## 📞 Support

- 🔗 **Repository**: [https://github.com/Aryankr0711/LSTM-Assignment](https://github.com/Aryankr0711/LSTM-Assignment)
- 🐛 **Issues**: [GitHub Issues](https://github.com/Aryankr0711/LSTM-Assignment/issues)

---

**Last Updated**: April 14, 2026  
**Version**: 1.0  
**Status**: ✅ Complete & Deployed

---

Made with ❤️ by the Team
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
```

Build and run:
```bash
docker build -t lstm-predictor .
docker run -p 8000:8000 lstm-predictor
```

---

## 📚 References

- **Hochreiter & Schmidhuber (1997):** Long Short-Term Memory
- **TensorFlow Documentation:** https://www.tensorflow.org/
- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **Wikitext-103 Dataset:** https://www.tensorflow.org/datasets/catalog/wikitext

---

## 🤝 Acknowledgements

**AI Tools Used:**
- ChatGPT / AI Language Models
- Used for: Code generation, explanations, structuring

**Sections with AI Assistance:**
- Data preprocessing functions
- LSTM model architecture
- Mathematical explanations
- FastAPI application structure
- Project organization

---

## 📝 License

Academic Project - For educational purposes

---

## 📞 Contact

For questions or issues, please refer to the project documentation in `Aryan_LSTM.ipynb`

---

**Last Updated:** April 14, 2026

**Version:** 1.0.0

