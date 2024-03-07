"""pmlops configuration module.

"""

from pydantic.dataclasses import dataclass


@dataclass
class ModelConfig:
    """
    Model configuration class

    """

    ml_artifact: str
    features: list
