"""
This module is just a convenience to train a simple classifier.
Its presence is a bit artificial for the exercice and not required to develop an MLOps platform.
The MLOps course is not about model training.
"""

from dataclasses import dataclass
import logging
import pandas as pd
import xgboost as xgb
from datetime import datetime
from sklearn.base import ClassifierMixin, RegressorMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from dsba.model_registry import ClassifierMetadata
from .preprocessing import split_features_and_target, preprocess_dataframe


# def train_simple_classifier(
#     df: pd.DataFrame, target_column: str, model_id: str
# ) -> tuple[ClassifierMixin, ClassifierMetadata]:
#     logging.info("Start training a simple classifier")
#     df = preprocess_dataframe(df)
#     X, y = split_features_and_target(df, target_column)
#     model = xgb.XGBClassifier(random_state=42)
#     model.fit(X, y)

#     logging.info("Done training a simple classifier")
#     metadata = ClassifierMetadata(
#         id=model_id,
#         created_at=str(datetime.now()),
#         algorithm="xgboost",
#         target_column=target_column,
#         hyperparameters={"random_state": 42},
#         description="",
#         performance_metrics={},
#     )
#     return model, metadata

def train_simple_classifier(
    df: pd.DataFrame, target_column: str, model_id: str, algorithm: str
) -> tuple[ClassifierMixin, ClassifierMetadata]:
    logging.info(f"Start training with {algorithm}")
    
    df = preprocess_dataframe(df)
    X, y = split_features_and_target(df, target_column)
    
    if algorithm == "xgboost":
        model = xgb.XGBClassifier(random_state=42)
    elif algorithm == "random_forest":
        model = RandomForestClassifier(random_state=42)
    elif algorithm == "logistic_regression":
        model = LogisticRegression(random_state=42)
    elif algorithm == "svm":
        model = SVC(random_state=42, probability=True)
    elif algorithm == "decision_tree":
        model = DecisionTreeClassifier(random_state=42)
    else:
        raise ValueError(f"Algorithm '{algorithm}' not supported. Choose from ['xgboost', 'random_forest', 'logistic_regression', 'svm', 'decision_tree'].")
    
    model.fit(X, y)
    
    logging.info("Done training")
    
    metadata = ClassifierMetadata(
        id=model_id,
        created_at=str(datetime.now()),
        algorithm=algorithm,
        target_column=target_column,
        hyperparameters={"random_state": 42},
        description="",
        performance_metrics={},
    )
    
    return model, metadata