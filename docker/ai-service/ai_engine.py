import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

class AIEngine:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.is_trained = False

    def train_mock_model(self):
        """Train on synthetic normal data"""
        # Generate normal data: 50% GPU load, 60C temp
        X_train = np.random.normal(loc=[50, 60], scale=[10, 5], size=(1000, 2))
        self.model.fit(X_train)
        self.is_trained = True
        return "Model Trained"

    def predict(self, gpu_util, temp):
        if not self.is_trained:
            self.train_mock_model()
        
        # Data format: [[gpu, temp]]
        data = [[gpu_util, temp]]
        prediction = self.model.predict(data)[0]
        score = self.model.decision_function(data)[0]
        
        # -1 is anomaly, 1 is normal
        is_anomaly = True if prediction == -1 else False
        
        # Simple RCA Logic
        cause = "Normal"
        if is_anomaly:
            if temp > 80: cause = "Thermal Throttling"
            elif gpu_util > 90: cause = "Compute Saturation"
            else: cause = "Unknown/Statistical Deviation"
            
        return is_anomaly, score, cause
