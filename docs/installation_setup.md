# Installation & Setup

### Prerequisites

- You must have Python installed.
- You must have `pip` installed.
- You must have Docker installed.
- You need VS Code.

### AWS Prerequisites

- You must have the AWS CLI installed and an AWS account with an access key and secret key stored in `~/.aws/credentials`:
    - Create a new user:
        ```bash
        aws iam create-user --user-name MyIAMUser
        ```
    - Attach policies to this user:
    
        ```bash
        aws iam attach-user-policy --user-name MyIAMUser --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess
        aws iam attach-user-policy --user-name MyIAMUser --policy-arn arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess
        aws iam attach-user-policy --user-name MyIAMUser --policy-arn arn:aws:iam::aws:policy/AmazonECS_FullAccess
        aws iam attach-user-policy --user-name MyIAMUser --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
        aws iam attach-user-policy --user-name MyIAMUser --policy-arn arn:aws:iam::aws:policy/AWSAppRunnerFullAccess
        aws iam attach-user-policy --user-name MyIAMUser --policy-arn arn:aws:iam::aws:policy/IAMFullAccess
        aws iam attach-user-policy --user-name MyIAMUser --policy-arn arn:aws:iam::aws:policy/IAMReadOnlyAccess
        ```
    - Create an IAM Role:
    
        ```bash
        aws iam create-role --role-name AppRunnerECRAccessRole \
        --assume-role-policy-document '{
            "Version": "2012-10-17",
            "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                "Service": "build.apprunner.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
            ]
        }'
        ```
    - Attach policies to this role:
    
        ```bash
        aws iam attach-role-policy --role-name AppRunnerECRAccessRole --policy-arn arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess
        aws iam attach-role-policy --role-name AppRunnerECRAccessRole --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess
        ```

    ```bash
    aws iam get-role --role-name AppRunnerECRAccessRole --query 'Role.Arn' --output text
    ```

    
    - Create an access key:
        
        ```bash
        aws iam create-access-key --user-name MyIAMUser
        ```

    
    - Add the access key and secret key to the AWS CLI using the elements `AccessKeyId` and `SecretAccessKey` generated previously:

        ```bash
        aws configure --profile MyIAMUser
        ```
    

- You need to create a S3 bucket:

    ```bash
    aws s3api create-bucket --bucket dsba-mlops-project --region eu-west-3 --create-bucket-configuration LocationConstraint=eu-west-3 --profile MyIAMUser
    ```

    - Notes:
        - You can chose a different bucket name but you will need to update the `.env` file mentioned at step 5 of the installation accordingly.
        - You can check that the bucket was created by running `aws s3 ls`.

___

### Installation

1. **Download the repository**
    - Go to [mlops-project](https://github.com/allisterk2703/mlops-project).
    - Click on "Code", then "Download ZIP".
    - Extract the ZIP file to your `~/Desktop` for easy access.

    Or clone the repository using the following command:

    ```bash
    cd Desktop
    git clone https://github.com/allisterk2703/mlops-project.git
    ```

2. **Open the project in VS Code**
    - Open the `mlops-project` folder in VS Code.
    - Open a terminal in VS Code: Press `Control ^` + `Shift ⇧` + `<`.

3. **Set up the virtual environment**
    
    Run the following commands in the terminal:
    
    ```bash
    pip install hatch
    hatch env create
    hatch shell
    pip install -e .
    ```

4. **Set environment variables**

    To ensure the correct paths are recognized, add the following lines to your `~/.zshrc` file:
    
    ```bash
    echo 'export PYTHONPATH="$PYTHONPATH:$HOME/Desktop/dsba-platform/src"' >> ~/.zshrc
    echo 'export DSBA_MODELS_ROOT_PATH="$HOME/Desktop/dsba-platform/models"' >> ~/.zshrc
    ```
    
    Then, run the following command to apply the changes:
    
    ```bash
    source ~/.zshrc
    ```

5. **Create a `.env` file**
    
    At the root of the project, create a `.env` file and add the following (using the AWS credentials and S3 bucket name you created earlier):
    
    ```bash
    AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY_ID>
    AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_ACCESS_KEY>
    AWS_REGION=<YOUR_AWS_REGION>
    S3_BUCKET_NAME=dsba-mlops-project
    ```

---