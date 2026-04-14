# 🚀 QUICK START GUIDE

## LSTM Next Word Prediction System - Start Here!

---

## ⚡ 5-Minute Setup

### 1. **Install Dependencies** (1 minute)
```bash
cd MDM_LSTM
pip install -r requirements.txt
```

### 2. **Run the Notebook** (2-3 minutes to load, 15-30 min to train)
```bash
jupyter notebook Aryan_LSTM.ipynb
```
Then run all cells by pressing **Ctrl+A** then **Shift+Enter**

### 3. **Start the API** (in a new terminal)
```bash
uvicorn app:app --reload
```

### 4. **Test It!** (1 minute)
Open in your browser: **http://localhost:8000/docs**

Or run Python script:
```bash
python api_examples.py
```

---

## 🎯 What You Get

| Component | File | Status |
|-----------|------|--------|
| 📓 Main Notebook | `Aryan_LSTM.ipynb` | ✅ Ready |
| 🌐 API Server | `app.py` | ✅ Ready |
| 🧪 Test Examples | `api_examples.py` | ✅ Ready |
| 📦 Dependencies | `requirements.txt` | ✅ Ready |
| 📚 Documentation | `README.md` | ✅ Ready |

---

## 📊 Project Structure

```
Aryan_LSTM.ipynb          ← RUN THIS FIRST (Jupyter notebook with all sections)
app.py                    ← FastAPI server (for deployment)
api_examples.py           ← Test the API (run after starting server)
requirements.txt          ← Install dependencies
README.md                 ← Full documentation
DEPLOYMENT_GUIDE.md       ← Deployment instructions
PROJECT_STRUCTURE.md      ← File organization
DELIVERY_SUMMARY.md       ← What's included
QUICK_START.md            ← This file
.gitignore               ← Git ignore patterns
```

---

## 🔄 Typical Workflow

### First Time?
```
1. pip install -r requirements.txt
2. jupyter notebook Aryan_LSTM.ipynb
3. Run all cells (Ctrl+A, Shift+Enter)
4. Wait for training to complete
```

### Testing the API?
```
1. In another terminal: uvicorn app:app --reload
2. Browser: http://localhost:8000/docs
3. Or: python api_examples.py
```

### Need to Deploy?
```
1. Read DEPLOYMENT_GUIDE.md
2. Choose option (Gunicorn, Docker, Cloud)
3. Follow instructions
```

---

## 🎓 Inside the Notebook

The Jupyter notebook has **11 main sections**:

| Section | What | Time |
|---------|------|------|
| 1️⃣ Introduction | LSTM basics | 2 min read |
| 2️⃣ Libraries | Setup | 1 min run |
| 3️⃣ Dataset | Load Wikitext-103 | 5 min run |
| 4️⃣ Preprocessing | Clean text | 5 min run |
| 5️⃣ Model | Build LSTM | 1 min run |
| 6️⃣ Math | Equations & formulas | 5 min read |
| 7️⃣ Training | Train model | 20 min run |
| 8️⃣ Predict | Inference function | 1 min run |
| 9️⃣ FastAPI | API code | 1 min read |
| 🔟 Testing | Test examples | 5 min run |
| 1️⃣1️⃣ Conclusion | Summary | 2 min read |

---

## 💻 Example Commands

### Test with cURL
```bash
# Single prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"the quick brown fox","top_k":5}'

# Health check
curl http://localhost:8000/health

# Model info
curl http://localhost:8000/info
```

### Test with Python
```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={"text": "machine learning is", "top_k": 3}
)
print(response.json())
```

### Test with Swagger UI
1. Go to http://localhost:8000/docs
2. Click on POST /predict
3. Click "Try it out"
4. Enter your text
5. Click "Execute"

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| `pip install fails` | Use `pip install --upgrade pip` first |
| `Port 8000 already in use` | Kill process or use `--port 8001` |
| `ModuleNotFoundError: No module named 'tensorflow'` | Run `pip install -r requirements.txt` again |
| `Jupyter command not found` | Install with `pip install jupyter` |
| `API gives 503 error` | Make sure notebook ran successfully to generate model files |
| `Slow predictions` | Use GPU if available or wait for results |

---

## 📈 Expected Results

After running the notebook, you should see:

✅ Model successfully trained  
✅ Training and validation loss curves  
✅ Accuracy metrics displayed  
✅ Sample predictions generated  
✅ Model saved as `lstm_model.h5`  
✅ Tokenizer saved as `tokenizer.json`  

Then with API running:

✅ FastAPI starts successfully  
✅ Swagger UI accessible at http://localhost:8000/docs  
✅ Health check returns `{"status":"healthy"}`  
✅ Predictions returned with confidence scores  
✅ Examples work without errors  

---

## 📚 Documentation

For more details, read:

- **README.md** - Full project overview
- **DEPLOYMENT_GUIDE.md** - How to deploy
- **PROJECT_STRUCTURE.md** - Files explained
- **DELIVERY_SUMMARY.md** - What's included

---

## 🎯 Common Tasks

### "I want to train the model"
```bash
jupyter notebook Aryan_LSTM.ipynb
# Run all cells from Section 1-7
```

### "I want to use the API"
```bash
uvicorn app:app --reload
# Go to http://localhost:8000/docs
```

### "I want to deploy to production"
```bash
# Read DEPLOYMENT_GUIDE.md and follow the Gunicorn section
```

### "I want to test predictions"
```bash
python api_examples.py
```

### "I want to understand LSTM math"
```
# See Section 6 in Aryan_LSTM.ipynb for equations
```

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Installation | 2-5 min |
| Initial setup | 1-2 min |
| Reading intro section | 5 min |
| Loading dataset | 5-10 min |
| Preprocessing | 5-10 min |
| Training model | 15-30 min |
| API startup | < 1 min |
| First prediction | < 1 min |
| **Total Time** | **45 min - 1 hour** |

---

## 🎓 Team Information

| Name | PRN | Batch |
|------|-----|-------|
| Siddhant Sahu | 202301070159 | T3 |
| Aryan Kumar | 202301070164 | T1 |
| Amir Furquani | 202301070165 | T1 |
| Aryan Kumar | 202301070167 | T4 |

---

## ✨ Features

✅ Complete LSTM model with 2 layers  
✅ Wikitext-103 dataset integration  
✅ Advanced preprocessing pipeline  
✅ Mathematical explanations with equations  
✅ Production-ready FastAPI server  
✅ Comprehensive documentation  
✅ Ready-to-run code (no modifications needed)  
✅ Multiple deployment options  
✅ Error handling and validation  
✅ Batch prediction support  

---

## 🚀 Next Steps

1. **First time?** → Run the notebook
2. **Want to test?** → Start the API
3. **Need to deploy?** → Read DEPLOYMENT_GUIDE.md
4. **Have questions?** → Check documentation files
5. **Ready to submit?** → All files are ready!

---

## 📞 Help

- 📖 Notebook: `Aryan_LSTM.ipynb`
- 📚 Docs: `README.md`
- 🚀 Deploy: `DEPLOYMENT_GUIDE.md`
- 📋 Structure: `PROJECT_STRUCTURE.md`
- 🎯 Examples: `api_examples.py`

---

**Status:** ✅ COMPLETE & READY TO USE

**Happy coding! 🎉**

