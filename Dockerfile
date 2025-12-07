FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies from requirements file
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

# Expose the correct port
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]
