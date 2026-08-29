import numpy as np
from sklearn.ensemble import IsolationForest
from typing import List, Dict

class AnomalyDetector:
    """Unsupervised Anomaly Detection using Isolation Forest on security feature vectors."""

    def __init__(self, contamination: float = 0.05):
        self.contamination = contamination
        self.model = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=42,
            n_jobs=-1
        )
        self.is_fitted = False
        self._bootstrap_baseline_model()

    def _bootstrap_baseline_model(self):
        """Generates realistic normal baseline telemetry and fits the Isolation Forest model."""
        np.random.seed(42)
        n_samples = 1500

        # Normal baseline distribution:
        # [login_failures_60s, unique_usernames, requests_per_min, ports_scanned, endpoint_diversity, auth_fail_ratio]
        normal_fails = np.random.poisson(lam=0.3, size=n_samples)
        normal_users = np.random.choice([0, 1], size=n_samples, p=[0.75, 0.25])
        normal_reqs = np.random.normal(loc=25, scale=12, size=n_samples).clip(0, 120)
        normal_ports = np.random.choice([0, 1, 2], size=n_samples, p=[0.8, 0.15, 0.05])
        normal_entropy = np.random.uniform(1.0, 5.0, size=n_samples)
        normal_fail_ratio = np.random.beta(a=0.5, b=10, size=n_samples)

        X_baseline = np.column_stack([
            normal_fails,
            normal_users,
            normal_reqs,
            normal_ports,
            normal_entropy,
            normal_fail_ratio
        ])

        self.model.fit(X_baseline)
        self.is_fitted = True

    def compute_anomaly_score(self, feature_vector: List[float]) -> float:
        """
        Computes anomaly score scaled between 0.0 (strictly normal) and 1.0 (highly anomalous).
        """
        if not self.is_fitted:
            self._bootstrap_baseline_model()

        X = np.array([feature_vector])
        # decision_function gives negative score for outliers, positive for inliers
        raw_score = self.model.decision_function(X)[0]
        
        # Sigmoid-style transformation to 0.0 - 1.0
        # raw_score typically spans [-0.3, 0.3]
        normalized_score = 1.0 / (1.0 + np.exp(raw_score * 8.0))
        return float(np.clip(normalized_score, 0.0, 1.0))
