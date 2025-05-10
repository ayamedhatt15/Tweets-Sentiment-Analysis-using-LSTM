from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences
from gensim.models import Word2Vec
import joblib
import json

app = FastAPI(
    title="Sentiment Analysis API",
    description="API for sentiment analysis using LSTM",
    version="1.0.0"
)

# Model initialization
try:
    # NLTK setup
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    stop_words.remove('not')
    
    # Load artifacts
    tokenizer = joblib.load('tokenizer.pkl')
    w2v_model = Word2Vec.load("word2vec.model")
    
    # Load model architecture
    with open('model_architecture.json', 'r') as f:
        model_config = f.read()  # Read the JSON string
        model = model_from_json(model_config)  # Directly pass the string without decoding

    # Load model weights
    model.load_weights('model_weights.h5')
    
    # Load label encoder
    labelencoder = joblib.load('labelencoder.pkl')
    
    print("All components loaded successfully!")

except Exception as e:
    print(f"Initialization error: {str(e)}")
    raise RuntimeError("Failed to load critical components")

class TextRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    sentiment: str
    confidence: float

def preprocess(text: str):
    # Match notebook preprocessing exactly
    text_clean = re.sub(r'@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+', ' ', text.lower())
    text_clean = ' '.join([word for word in text_clean.split() if word not in stop_words])
    sequence = tokenizer.texts_to_sequences([text_clean])
    padded = pad_sequences(sequence, maxlen=300)
    return padded

@app.get("/")
def read_root():
    return {"message": "Sentiment Analysis API"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "components": {
            "model": model is not None,
            "tokenizer": tokenizer is not None,
            "word2vec": w2v_model is not None
        }
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: TextRequest):
    try:
        processed = preprocess(request.text)
        prediction = model.predict(processed)
        label_index = np.argmax(prediction[0])
        return PredictionResponse(
            sentiment=labelencoder.classes_[label_index],
            confidence=float(prediction[0][label_index])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)