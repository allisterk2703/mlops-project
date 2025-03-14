import json
import os
import pandas as pd
import json
import logging
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from dsba.model_registry import list_models_ids, load_model, load_model_metadata
from dsba.model_prediction import classify_record
from dsba.model_registry import list_models_ids, _get_models_dir, _list_pickle_files
from typing import Dict, Any
from dotenv import load_dotenv
load_dotenv()

# class TitanicFeatures(BaseModel):
#     PassengerId: int
#     Pclass: int
#     Name: str
#     Sex: int
#     Age: float
#     SibSp: int
#     Parch: int
#     Ticket: int
#     Fare: float
#     Cabin: int
#     Embarked: int


class PredictRequest(BaseModel):
    model_id: str
    query: Dict[str, Any]


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S,",
)

app = FastAPI()

# using FastAPI with defaults is very convenient
# we just add this "decorator" with the "route" we want.
# If I deploy this app on "https//mywebsite.com", this function can be called by visiting "https//mywebsite.com/models/"


@app.get("/models/")
async def list_models(dataset: str = Query(..., description="Dataset name")):
    return list_models_ids(dataset)


def useful_column_types(path):
    dataset = path.split("/")[1]
    with open(path, "r") as f:
        lines = [line.strip() for line in f]
    return lines


@app.get("/get_coltypes/")
async def get_coltypes(dataset: str):
    try:
        template = useful_column_types(f"models/{dataset}/useful_columns.txt")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return template


@app.post("/predict/")
async def predict(request: PredictRequest):
    try:
        model = load_model(request.model_id)
        metadata = load_model_metadata(request.model_id)
        prediction = classify_record(
            model, request.query, metadata.target_column)
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict_with_best_model/")
async def predict_with_best_model(request: PredictRequest):
    try:
        with open(f"models/{request.model_id}/best_model.txt", "r") as f:
            lines = f.readlines()
        best_model = lines[0].strip()
        trained_on = lines[1].strip()[:-4]
        pickle = f"{request.model_id}/{trained_on}_{best_model}"

        model = load_model(pickle)
        metadata = load_model_metadata(pickle)
        prediction = classify_record(
            model, request.query, metadata.target_column)
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
