# User Guide

### Add a Dataset

Allows adding a dataset to the tool.

- **Parameters:**
    - `--name` (required): Name assigned to the dataset when adding it.
    - `--file`: Path to a local file containing the dataset.
    - `--url`: URL of a remote source to fetch the dataset.
    - `--new`: Indicates that this is a **new dataset** (should not be included when adding a new version of an existing dataset).
    - `--upload_on_s3` (optional): Indicates whether to upload the dataset to the S3 bucket (if present, the dataset will be uploaded).

    **Notes:**

    - Either `--file` or `--url` must be specified, but not both simultaneously.
    - The `--new` flag is required to add a dataset that does not yet exist.
    
- **Examples:**
    
    - Add a dataset from a URL and add it to the S3 bucket (recommended for an easy demo 🙌):
        
        ```bash
        python src/cli/dsba_cli save_dataset --name titanic --url https://www.kaggle.com/api/v1/datasets/download/yasserh/titanic-dataset --upload_on_s3
        ```

        *⚠️ Note: To download datasets from Kaggle, ensure you have your Kaggle API key stored in `~/.kaggle/kaggle.json` (https://www.kaggle.com/docs/api#authentication).*
    
    - Add a dataset from a local file (and not upload it to the S3 bucket):
        
        ```bash
        python src/cli/dsba_cli save_dataset --name titanic --file /Users/allisterkohn/Desktop/titanic.csv
        ```
        

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

Displays the list of datasets available for download stored in your S3 bucket.

- **Example:**
    
    ```bash
    python src/cli/dsba_cli list_s3_datasets
    ```
    

### Display Versions of a Specific S3 Dataset

Lists all versions of a specific dataset stored in the S3 bucket.

- **Parameter:**
    - `--dataset` (required): Name of the dataset.
- **Example:**
    
    ```bash
    python src/cli/dsba_cli list_s3_dataset_versions --dataset titanic
    ```
    

### Download a Dataset from S3

Allows retrieving a dataset stored in your S3 bucket and downloading it to the local environment.

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
    - `--test_size` (optional, default: `0.2`): Size of the test set.
    
    **Note:**
    
    - If `--useless` is not specified, no columns will be removed.

- **Example:**
    
    ```bash
    python src/cli/dsba_cli preprocess --dataset titanic/titanic_v1_2025-03-01_14-29.csv --target Survived --mode mode --useless PassengerId Name Ticket
    ```
    

### Train a Model

Allows training a model after dataset preprocessing.

- **Parameters:**
    - `--dataset` (required): Path to the preprocessed dataset.
    - `--target` (required): Name of the target variable.
    - `--model` (required): Machine learning model to use (available models: `xgboost`, `random_forest`, `logistic_regression`, `svm`, `decision_tree`, `all`).
    - `--gridsearch` (optional, default: `False`): Indicates whether to use GridSearch to find the best hyperparameters.
- **Examples:**
    - Train an XGBoost model without GridSearch:
        
        ```bash
        python src/cli/dsba_cli train --dataset preprocessed_datasets/titanic/titanic_v1_2025-03-01_14-29 --target Survived --model xgboost
        ```
        
    - Train all available models with GridSearch (recommended for a full demo 🙌)
        
        ```bash
        python src/cli/dsba_cli train --dataset preprocessed_datasets/titanic/titanic_v1_2025-03-01_14-29 --target Survived --model all --gridsearch
        ```
        

### Preprocess a Dataset and Train a Model (combined)

Performs dataset preprocessing and trains a model in a single command.

- **Parameters:**
    - `--dataset` (required): Path to the dataset to preprocess.
    - `--target` (required): Name of the target variable.
    - `--mode` (required): Method for filling missing values (available modes: `mean`, `median`, `most_frequent`, `constant`).
    - `--model` (required): Machine learning model to use (available models: `xgboost`, `random_forest`, `logistic_regression`, `svm`, `decision_tree`, `all`).
    - `--useless` (optional): List of columns to exclude from the dataset (separated by spaces).
    - `--test_size` (optional, default: `0.2`): Size of the test set.
    - `--gridsearch` (optional, default: `False`): Indicates whether to use GridSearch to find the best hyperparameters.
- **Example:**

    - Train an XGBoost model on a preprocessed dataset without GridSearch:
    
        ```bash
        python src/cli/dsba_cli preprocess_and_train --dataset titanic/titanic_v1_2025-03-01_14-29.csv --target Survived --mode mode --model xgboost --useless PassengerId Name Ticket
        ```

    - Train all available models with GridSearch (recommended for a full demo 🙌):
    
        ```bash
        python src/cli/dsba_cli preprocess_and_train --dataset titanic/titanic_v1_2025-03-01_14-29.csv --target Survived --mode mode --model all --useless PassengerId Name Ticket --gridsearch
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
    - `--useless` (optional): List of columns to exclude from the dataset (separated by spaces).

- **Example:**
    
    ```bash
    python src/cli/dsba_cli predict --input titanic_test.csv --output predictions.csv --model titanic/titanic_v1_2025-03-01_14-29_random_forest
    ```
    

### Make a Prediction with the Best Model

Automatically uses the best available model to make a prediction.

- **Parameters:**
    - `--input` (required): Path to the test file.
    - `--output` (required): Path to the output file for the predictions.
    - `--dataset` (required): Name of the dataset containing the model to use.
    - `--useless` (optional): List of columns to exclude from the dataset (separated by spaces).
    - `--metric` (optional, default: `f1_score`): Model evaluation metric (available metrics: `accuracy`, `precision`, `recall`, `f1_score`).

- **Example:** Make a prediction with the best model based on the Precision metric:
    
    ```bash
    python src/cli/dsba_cli predict_with_best_model --input titanic_test.csv --output predictions.csv --dataset titanic --metric precision
    ```


### Build image

Builds a Docker image for the project.

```bash
python src/cli/dsba_cli build_image
```


### Create an ECR Repository

Creates an Amazon Elastic Container Registry (ECR) repository to store Docker images.

- **Parameters:**

    - `--repository-name` (optional, default: `mlopsapprunner`): The name of the ECR repository to create.

- **Example:**

    ```bash
    python src/cli/dsba_cli create_ecr_repository
    ```
    This command returns the URI that will be necessary in the next step.

### Tag and Push a Docker Image to ECR
Tags a local Docker image and pushes it to the ECR repository.

- **Parameters:**

    - `--repository_uri` (required): The URI of the ECR repository where the image will be pushed.

- **Example:**

    ```bash
    python src/cli/dsba_cli tag_and_push_image --repository-uri 217831684037.dkr.ecr.eu-west-3.amazonaws.com/mlopsapprunner
    ```


### Deploy an ECR Image to AWS App Runner

Deploys a Docker image from ECR to AWS App Runner,automatically configuring environment variables.

- **Parameters:**

    - `--image-identifier` (required): The ECR image URI (including tag) to deploy.

    - `--service-name` (optional, default: `mlops-app-runner`): The name of the App Runner service.

- **Example:**

    ```bash
    python src/cli/dsba_cli deploy_from_ecr_to_app_runner --image-identifier <YOUR_REPOSITORY_URI>:latest --service-name my-app-service
    ```


___

### Display the list of available models for a specific dataset

Fetches the list of available models trained on a given dataset.

- **Endpoint:** `<YOUR_DOMAIN>/models/?dataset=<dataset_name>`

- **Example :** `curl -X GET "https://gpfyyj2xmp.eu-west-3.awsapprunner.com/models/?dataset=titanic"`


### Retrieve the data and their types to send for a request to a model

Returns the column names and their respective data types for a given dataset. This helps structure requests correctly when making predictions.

- **Endpoint:** `<YOUR_DOMAIN>/get_coltypes/?dataset=<dataset_name>`

- **Example:** `curl -X GET "https://gpfyyj2xmp.eu-west-3.awsapprunner.com/get_coltypes/?dataset=titanic"`

### Make a prediction using a specific model trained on a specific dataset

- **Endpoint:** `<YOUR_DOMAIN>/predict/`
- **Examples:**

    - With cURL:
        
        ```bash
        curl -X POST "http://127.0.0.1:8000/predict/" \
            -H "Content-Type: application/json" \
            -d '{
                "model_id": "titanic/titanic_v2_2025-04-01_14-29_random_forest",
                "query": {
                    "Pclass": 3,
                    "Sex": 1,
                    "Age": 22.0,
                    "SibSp": 1,
                    "Parch": 0,
                    "Fare": 7.25,
                    "Cabin": 3,
                    "Embarked": 2
                }
            }'
        ```
    

    - With Python:
        
        ```python
        import requests
        
        url = "http://127.0.0.1:8000/predict/"
        data = {
            "model_id": "titanic/titanic_v2_2025-04-01_14-29_random_forest",
            "query": {
                "Pclass": 3,
                "Sex": 1,
                "Age": 22.0,
                "SibSp": 1,
                "Parch": 0,
                "Fare": 7.25,
                "Cabin": 3,
                "Embarked": 2
            }
        }
        response = requests.post(url, json=data)
        print(response.json())
        ```

### **Make a prediction using the best model trained on a specific dataset**

- **Endpoint:** `<YOUR_DOMAIN>/predict_with_best_model/`
- **Examples:**
    - With cURL:
        
        ```bash
        curl -X POST "http://127.0.0.1:8000/predict_with_best_model/" \
            -H "Content-Type: application/json" \
            -d '{
                "model_id": "titanic",
                "query": {
                    "Pclass": 3,
                    "Sex": 1,
                    "Age": 22.0,
                    "SibSp": 1,
                    "Parch": 0,
                    "Fare": 7.25,
                    "Cabin": 3,
                    "Embarked": 2
                }
            }'
        ```
    
    - With Python:
        
        ```python
        import requests
        
        url = "http://127.0.0.1:8000/predict_with_best_model/"
        data = {
            "model_id": "titanic",
            "query": {
                "Pclass": 3,
                "Sex": 1,
                "Age": 22.0,
                "SibSp": 1,
                "Parch": 0,
                "Fare": 7.25,
                "Cabin": 3,
                "Embarked": 2
            }
        }
        response = requests.post(url, json=data)
        print(response.json())
        ```
        
---