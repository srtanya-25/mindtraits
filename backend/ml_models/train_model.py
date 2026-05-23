"""
ml_models/train_model.py
Trains an XGBoost classifier on synthetic Big Five data and saves model.pkl.
Run: python train_model.py
"""
import os
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

try:
    from xgboost import XGBClassifier
except ImportError:
    raise ImportError("Install xgboost: pip install xgboost")

#  Synthetic dataset 
np.random.seed(42)
N = 1000

# Each row: [O, C, E, A, N] scores (4 questions × max 5 = 20 max per trait)
data = np.random.randint(4, 21, size=(N, 5)).astype(float)

# Label by dominant trait
labels_map = {0: 'Creative Explorer', 1: 'Organized Achiever', 2: 'Social Dynamo',
              3: 'Empathetic Helper', 4: 'Sensitive Thinker'}
raw_labels = np.argmax(data, axis=1)

# Encode as integers for XGBoost
label_to_int = {v: k for k, v in labels_map.items()}
y = raw_labels  # already 0-4

X_train, X_test, y_train, y_test = train_test_split(data, y, test_size=0.2, random_state=42)

model = XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.1, use_label_encoder=False, eval_metric='mlogloss')
model.fit(X_train, y_train)

print(classification_report(y_test, model.predict(X_test),
                             target_names=list(labels_map.values())))

model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"Model saved to {model_path}")
