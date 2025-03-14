# Developer Documentation

## FastAPI

- **Launch the API**
    
    ```bash
    fastapi dev src/api/api.py
    ```

- **Display the list of available models for a specific dataset**

    *Endpoint:* `http://127.0.0.1:8000/models/?dataset=<dataset_name>`

- **Retrieve the data and their types to send for a request to a model**

    *Endpoint:* `http://127.0.0.1:8000/get_coltypes/?dataset=<dataset_name>`

- **Make a prediction using a specific model trained on a specific dataset**

    *Endpoint:* `http://127.0.0.1:8000/predict/`

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

- **Make a prediction using the best model trained on a specific dataset**

    *Endpoint:* `http://127.0.0.1:8000/predict_with_best_model/`

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


## Docker

(Commands to run in the project root directory)

- **Build the image**
    - ARM64 architecture:
        
        ```bash
        docker build -t fastapi-app -f src/api/Dockerfile .
        ```
        
    - AMD64 architecture:
        
        ```bash
        docker buildx build --platform linux/amd64 -t fastapi-app -f src/api/Dockerfile . --load
        ```
        
- **Run the container**
    
    ```bash
    docker run -d --platform linux/amd64 -p 8000:8000 --name fastapi-container \
      -v "/Users/allisterkohn/Desktop/DSBA/T2 - Data Sciences Electives/MLOps/Project/dsba-platform/models:/app/models" \
      -e DSBA_MODELS_ROOT_PATH="/app/models" \
      --env-file .env \
      fastapi-app
    ```
    
    (If the `.env` file is stored somewhere other than the project root, provide the full path)

    - If the container `fastapi-container` already exists, use:
        
        ```bash
        docker rm -f fastapi-container
        ```
        
        Then re-run the  `docker run` command.
        
- **Display the environment variables of the container**
    
    ```bash
    docker exec -it fastapi-container env
    ```
    
- **Tag the image for AWS ECR**
    
    ```bash
    docker tag fastapi-app 217831684037.dkr.ecr.eu-west-3.amazonaws.com/mlops-app-runner:latest
    ```
    
- **Authenticate with AWS**
    
    ```bash
    aws ecr get-login-password --region eu-west-3 | docker login --username AWS --password-stdin 217831684037.dkr.ecr.eu-west-3.amazonaws.com
    ```
    
- **Create a repository on AWS ECR**
    
    ```bash
    aws ecr create-repository --repository-name mlops-app-runner --region eu-west-3
    ```
    
- **Push the image to this repository**
    
    ```bash
    docker push 217831684037.dkr.ecr.eu-west-3.amazonaws.com/mlops-app-runner:latest
    ```
    
- **Create an AWS App Runner service**
    
    ```bash
    aws apprunner create-service --service-name mlops-app-runner \
        --region eu-west-3 \
        --profile s3-user \
        --source-configuration '{
            "AuthenticationConfiguration": {
                "AccessRoleArn": "arn:aws:iam::217831684037:role/service-role/AppRunnerECRAccessRole"
            },
            "ImageRepository": {
                "ImageIdentifier": "217831684037.dkr.ecr.eu-west-3.amazonaws.com/mlops-app-runner:latest",
                "ImageRepositoryType": "ECR",
                "ImageConfiguration": {
                    "Port": "8000",
                    "RuntimeEnvironmentVariables": {
                        "DSBA_MODELS_ROOT_PATH": "/app/models"
                    }
                }
            },
            "AutoDeployments": true
        }'
    ```
    
- **Retrieve the `ServiceURI` of the deployed service**
    
    ```bash
    aws apprunner list-services --region eu-west-3 --profile s3-user
    ```
    

---

## AWS

- **Install the AWS CLI:** `brew install awscli`
- **Connect to any user of your AWS account:** `aws configure`
- **Create a new user**
    
    ```bash
    aws iam create-user --user-name MyIAMUser
    ```
    
- **Attach policies to this user**
    
    ```bash
    aws iam attach-user-policy --user-name MyIAMUser --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess
    aws iam attach-user-policy --user-name MyIAMUser --policy-arn arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess
    aws iam attach-user-policy --user-name MyIAMUser --policy-arn arn:aws:iam::aws:policy/AmazonECS_FullAccess
    aws iam attach-user-policy --user-name MyIAMUser --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
    aws iam attach-user-policy --user-name MyIAMUser --policy-arn arn:aws:iam::aws:policy/AWSAppRunnerFullAccess
    aws iam attach-user-policy --user-name MyIAMUser --policy-arn arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess
    aws iam attach-user-policy --user-name MyIAMUser --policy-arn arn:aws:iam::aws:policy/IAMFullAccess
    aws iam attach-user-policy --user-name MyIAMUser --policy-arn arn:aws:iam::aws:policy/IAMReadOnlyAccess
    ```
    
- **Create an access key**
    
    ```bash
    aws iam create-access-key --user-name MyIAMUser
    ```
    
- **Connect to the created user**
    
    ```bash
    aws configure
    ```

---