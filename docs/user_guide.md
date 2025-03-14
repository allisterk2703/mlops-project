# User Guide

## Features

### Add a Dataset

Allows adding a dataset to the tool.

- **Parameters:**
    - `--name` (required): Name assigned to the dataset when adding it.
    - `--file`: Path to a local file containing the dataset.
    - `--url`: URL of a remote source to fetch the dataset.
    - `--new`: Indicates that this is a **new dataset** (should not be included when adding a new version of an existing dataset).
- **Notes:**
    - Either `--file` or `--url` must be specified, but not both simultaneously.
    - The `--new` flag is required to add a dataset that does not yet exist.
- **Examples:**
    - Add a dataset from a local file:
        
        ```bash
        python src/cli/dsba_cli save_dataset --name titanic --file /Users/allisterkohn/Desktop/titanic.csv
        ```
        
    - Add a dataset from a URL:
        
        ```bash
        python src/cli/dsba_cli save_dataset --name titanic --url https://www.kaggle.com/api/v1/datasets/download/yasserh/titanic-dataset
        ```

        *Note: To download datasets from Kaggle, ensure you have your Kaggle API key stored in a `.kaggle/kaggle.json` file at the root of your project.*
        

### Display All Local Datasets

Displays the list of all datasets stored locally on the machine.

- **Example:**
    
    ```bash
    python src/cli/dsba_cli list_local_datasets
    ```
    

### Display Versions of a Specific Local Dataset

Lists all versions of a specific dataset stored locally.

- **Parameter:**
    - `--dataset` (required): Name of the dataset.
- **Example:**
    
    ```bash
    python src/cli/dsba_cli list_dataset_versions --dataset titanic
    ```
    

### Display All S3 Datasets

Displays the list of datasets stored in the S3 bucket `dsba-mlops-project-bucket`, available for download.

- **Example:**
    
    ```bash
    python src/cli/dsba_cli list_s3_datasets
    ```
    

### Display Versions of a Specific S3 Dataset …

Lists all versions of a specific dataset stored in the S3 bucket.

- **Parameter:**
    - `--dataset` (required): Name of the dataset.
- **Example:**
    
    ```bash
    python src/cli/dsba_cli list_s3_dataset_versions --dataset titanic
    ```
    

### Download a Dataset from S3

Allows retrieving a dataset stored in the S3 bucket `dsba-mlops-project-bucket` and downloading it to the local environment.

- **Parameter:**
    - `--s3_filename` (required): Name of the file as returned by the `list_s3_datasets` command.
- **Example:**
    
    ```bash
    python src/cli/dsba_cli download_dataset_from_S3 --s3_filename titanic/titanic_v1_2025-03-06_22-29.csv
    
    ```
    

### Preprocess a Dataset

Performs preprocessing on a dataset by filling missing values according to the specified mode and removing unnecessary columns.

- **Parameters:**
    - `--dataset` (required): Path to the dataset to preprocess.
    - `--target` (required): Name of the target variable.
    - `--mode` (required): Method for filling missing values (available modes: `mean`, `median`, `most_frequent`, `constant`).
    - `--useless` (optional): List of columns to exclude from the dataset (separated by spaces).
    
    **Note:**
    
    - If `--useless` is not specified, no columns will be removed.
- **Example:**
    
    ```bash
    python src/cli/dsba_cli preprocess --dataset titanic/titanic_v1_2025-03-01_14-29.csv --target Survived --mode mean --useless PassengerId Name Ticket
    ```
    

### Train a Model

Allows training a model after dataset preprocessing.

- **Parameters:**
    - `--dataset` (required): Path to the preprocessed dataset.
    - `--target` (required): Name of the target variable.
    - `--model` (required): Machine learning model to use (available models: `xgboost`, `random_forest`, `logistic_regression`, `svm`, `decision_tree`, `all`).
    - `--gridsearch` (optional, default: `False`): Indicates whether to use GridSearch to find the best hyperparameters.
- **Examples:**
    - Train an XGBoost model with GridSearch:
        
        ```bash
        python src/cli/dsba_cli train --dataset preprocessed_datasets/titanic/titanic_v1_2025-03-01_14-29 --target Survived --model xgboost --gridsearch
        ```
        
    - Train all available models without GridSearch:
        
        ```bash
        python src/cli/dsba_cli train --dataset preprocessed_datasets/titanic/titanic_v1_2025-03-01_14-29 --target Survived --model all
        ```
        

### Preprocess a Dataset and Train a Model

Performs dataset preprocessing and trains a model in a single command.

- **Parameters:**
    - `--dataset` (required): Path to the dataset to preprocess.
    - `--target` (required): Name of the target variable.
    - `--mode` (required): Method for filling missing values (available modes: `mean`, `median`, `most_frequent`, `constant`).
    - `--useless` (optional): List of columns to exclude from the dataset (separated by spaces).
    - `--model` (required): Machine learning model to use (available models: `xgboost`, `random_forest`, `logistic_regression`, `svm`, `decision_tree`, `all`).
    - `--gridsearch` (optional, default: `False`): Indicates whether to use GridSearch to find the best hyperparameters.
- **Example:**
    
    ```bash
    python src/cli/dsba_cli preprocess_and_train --dataset titanic/titanic_v1_2025-03-01_14-29.csv --target Survived --model xgboost --mode mean
    ```
    

### List Available Models

Displays the list of models associated with a specific dataset.

- **Parameter:**
    - `--dataset` (required): Name of the dataset.
- **Example:**
    
    ```bash
    python src/cli/dsba_cli list_models --dataset titanic
    ```
    

### Compare Models

Displays the performance metrics of trained models.

- **Parameter:**
    - `--dataset` (required): Name of the dataset.
- **Example:**
    
    ```bash
    python src/cli/dsba_cli compare_models --dataset titanic
    ```
    

### Find the Best Model for a Dataset

Tests multiple models and selects the one with the best performance based on the specified metric.

- **Parameters:**
    - `--dataset` (required): Name of the dataset.
    - `--metric` (optional, default: `f1_score`): Model evaluation metric (available metrics: `accuracy`, `precision`, `recall`, `f1_score`).
- **Example:**
    
    ```bash
    python src/cli/dsba_cli find_best_model --dataset titanic --metric f1_score
    ```
    
- **Notes:**
    
    The best model is saved in the `best_model.txt` file, which consists of three lines:
    
    - The name of the algorithm used.
    - Whether GridSearch was used or not.
    - The dataset on which the model was trained.

### Make a Prediction with a Specific Model

Predicts results from a test file and saves the predictions to an output file.

- **Parameters:**
    - `--input` (required): Path to the test file.
    - `--output` (required): Path to the output file for the predictions.
    - `--model` (required): Model to use for the prediction.
- **Example:**
    
    ```bash
    python src/cli/dsba_cli predict --input titanic_test.csv --output predictions.csv --model titanic/titanic_v1_2025-03-01_1_random_forest
    ```
    

### Make a Prediction with the Best Model

Automatically uses the best available model to make a prediction.

- **Parameters:**
    - `--input` (required): Path to the test file.
    - `--output` (required): Path to the output file for the predictions.
    - `--folder` (required): Name of the dataset containing the model to use.
- **Example:**
    
    ```bash
    python src/cli/dsba_cli predict_with_best_model --input titanic_test.csv --output predictions.csv --folder titanic
    ```
    

### Build image

Builds a Docker image for the project.

```bash
python src/cli/dsba_cli build_image
```

### Run container

Runs the Docker container.

```bash
python src/cli/dsba_cli run_container
```

---