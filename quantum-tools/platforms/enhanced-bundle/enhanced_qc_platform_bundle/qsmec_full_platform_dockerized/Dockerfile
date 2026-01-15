
FROM python:3.10-slim
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y build-essential git

# Install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app
COPY . .

# Run API by default
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
