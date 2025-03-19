# Use a lightweight Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install Hatch
RUN pip install --no-cache-dir hatch

# Copy only the necessary files for dependency installation
COPY pyproject.toml README.md ./

# Create the environment and install dependencies with Hatch
RUN hatch env create

# Copy the entire project into the container
COPY . .

# Add /app/src to PYTHONPATH
ENV PYTHONPATH="/app/src"

# Expose the API port
EXPOSE 8000

# Start the application using Hatch
CMD ["hatch", "run", "uvicorn", "src.api.api:app", "--host", "0.0.0.0", "--port", "8000"]