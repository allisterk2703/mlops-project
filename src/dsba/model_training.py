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
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from dsba.model_registry import ClassifierMetadata
from .preprocessing import split_features_and_target, preprocess_dataframe


def train_simple_classifier(df: pd.DataFrame, target_column: str, model_id: str, algorithm: str, dataset_name: str, gridsearch: bool = False) -> tuple[ClassifierMixin, ClassifierMetadata]:
    print("\n")
    logging.info(f"⏳ Start training with {algorithm} (GridSearch: {gridsearch})")

    df = preprocess_dataframe(df)
    X, y = split_features_and_target(df, target_column)

    param_grids = {
        "xgboost": {"n_estimators": [50, 100], "learning_rate": [0.01, 0.1]},
        "random_forest": {"n_estimators": [10, 50, 100]},
        "logistic_regression": {"clf__C": [0.01, 0.1, 1]},
        "svm": {"clf__C": [0.1, 1, 10]},
        "decision_tree": {"max_depth": [3, 5, None]}
    }

    base_models = {
        "xgboost": xgb.XGBClassifier(random_state=42),
        "random_forest": RandomForestClassifier(random_state=42),
        "logistic_regression": LogisticRegression(random_state=42),
        "svm": SVC(random_state=42, probability=True),
        "decision_tree": DecisionTreeClassifier(random_state=42)
    }
    try:
        model = base_models[algorithm]
    except:
        logging.error(f"❌ Invalid algorithm: {algorithm}")
        return None, None

    if algorithm in ["logistic_regression", "svm"]:
        model = Pipeline([("scaler", StandardScaler()), ("clf", model)])

    if (gridsearch == True) and (algorithm in param_grids):
        grid = GridSearchCV(model, param_grids[algorithm], cv=4, scoring='accuracy', n_jobs=-1)
        grid.fit(X, y)
        model = grid.best_estimator_
        best_params = grid.best_params_
    else:
        model.fit(X, y)
        best_params = {"random_state": 42}

    logging.info("✅ Training done")

    metadata = ClassifierMetadata(
        id=model_id,
        created_at=str(datetime.now()),
        algorithm=algorithm,
        target_column=target_column,
        hyperparameters=best_params,
        description="",
        performance_metrics={},
        gridsearch=gridsearch,
        dataset=dataset_name.split("/")[-1]
    )

    return model, metadata