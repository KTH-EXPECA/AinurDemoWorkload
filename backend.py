import pickle
import time

import numpy as np
from flask import Flask, request
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# load model
with open("training/forest.model", "rb") as fp:
    forest: RandomForestClassifier = pickle.load(fp)


@app.route("/classify", methods=["POST"])
def classify():
    ti = time.monotonic()
    image = np.frombuffer(request.get_data())
    label_probs = forest.predict_proba(np.atleast_2d(image))[0]
    label = np.argmax(label_probs)
    results = {
        "label": int(label),
        "confidence": float(label_probs[label]),
        "time": time.monotonic() - ti,
    }
    app.logger.info(f"Classifier results: {results}")
    return results
