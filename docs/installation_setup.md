# Installation & Setup

1. **Download the repository**
    - Go to [mlops-project](https://github.com/allisterk2703/mlops-project).
    - Click on "Code", then "Download ZIP"**.**
    - Extract the ZIP file to your desired location.
2. **Open the project in VS Code**
    - Open the extracted folder in ****VS Code.
    - Open a terminal: Press `Control ^` + `Shift ⇧` + `<`.
3. **Set up the virtual environment**
    
    Run the following commands in the terminal:
    
    ```bash
    python -m venv .venv  # Create a virtual environment
    source .venv/bin/activate  # Activate it
    pip install hatch  # Install Hatch for environment management
    hatch env create  # Create the environment with Hatch
    pip install -e .  # Install project dependencies
    ```
    
4. **Create a `.env` file**
    
    At the root of the project, create a `.env` file and add the following:
    
    ```bash
    AWS_ACCESS_KEY=<YOUR_AWS_ACCESS_KEY>
    AWS_SECRET_KEY=<YOUR_AWS_SECRET_KEY>
    AWS_REGION=<YOUR_AWS_REGION>
    S3_BUCKET_NAME=<YOUR_S3_BUCKET_NAME>
    ```

---