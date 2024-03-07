"""
pmlops inference module

"""

from functools import lru_cache

import joblib
import numpy as np
from pmlops.config import ModelConfig


@lru_cache(
    maxsize=100,
)
def load_ml_artifact(model_artifact: str) -> object:
    """
    Load a model artifact from a file

    Args:
    model_artifact (str): Path to the model artifact

    Returns:
    object: The model artifact
    """
    model = joblib.load(model_artifact)
    return model


def predict_from_artifact(config: ModelConfig) -> float:
    """
    Make a prediction using the MLflow endpoint

    Args:
    config (ModelConfig): The model configuration

    Returns:
    float: The prediction
    """

    model = load_ml_artifact(config.ml_artifact)
    prediction = model.predict(np.array(config.features).reshape(1, -1))[0]

    return prediction
