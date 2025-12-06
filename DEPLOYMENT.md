# Deployment Guide

This project is ready to be deployed on **Render** (or any other platform like Heroku/Railway).

## 1. Prerequisites

Ensure you have these files in your repository (I have already created/checked them):
- `app.py` (Main application)
- `requirements.txt` (Dependencies + gunicorn)
- `Procfile` (Start command)
- `model_pruned_float16.pkl` (The compressed model)

## 2. Deploy on Render.com

1.  **Push your code to GitHub**.
2.  Go to [Render Dashboard](https://dashboard.render.com/).
3.  Click **New +** -> **Web Service**.
4.  Connect your GitHub repository.
5.  **Settings**:
    - **Name**: `your-app-name`
    - **Runtime**: `Python 3`
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `gunicorn app:app` (Render might auto-detect this from Procfile)
6.  Click **Create Web Service**.

## 3. Model Handling

The model `model_pruned_float16.pkl` is **77 MB**, which is small enough to be pushed directly to GitHub.
- The application is configured to look for the model in the root directory automatically.
- **No extra configuration needed!** Just push and deploy.

## 4. Troubleshooting

If the build fails, check the logs. Common issues:
- **Python Version**: Render uses Python 3.7+ by default. This should work fine.
- **Memory**: The free tier has 512MB RAM. Since our model is only 77MB and we use `float16`, it should fit comfortably in memory.

## Local Testing

To test the production server locally (Windows):
```bash
# Install gunicorn (Linux/Mac) or waitress (Windows)
pip install waitress

# Run with waitress
waitress-serve --port=10000 app:app
```
