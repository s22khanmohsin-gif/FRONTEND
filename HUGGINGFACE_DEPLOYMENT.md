# Hugging Face Spaces Deployment Guide

Deploy your Flask ML application as a Docker Space on Hugging Face.

> [!IMPORTANT]
> Hugging Face Spaces offers **FREE hosting** for ML applications with generous resource limits. Perfect for showcasing your ML project!

## Prerequisites

✅ Your project now has:
- [`Dockerfile`](file:///c:/Users/mohat/OneDrive/Desktop/Frontend/Dockerfile) - Docker configuration
- [`README.md`](file:///c:/Users/mohat/OneDrive/Desktop/Frontend/README.md) - Space metadata & description
- [`.dockerignore`](file:///c:/Users/mohat/OneDrive/Desktop/Frontend/.dockerignore) - Optimize Docker builds
- [`app.py`](file:///c:/Users/mohat/OneDrive/Desktop/Frontend/app.py) - Flask application
- [`requirements.txt`](file:///c:/Users/mohat/OneDrive/Desktop/Frontend/requirements.txt) - Dependencies
- `model_pruned_float16.pkl` - ML model (77MB)

---

## Deployment Steps

### Method 1: Direct Upload (Easiest)

#### 1. Create a Space

1. Go to [Hugging Face](https://huggingface.co/)
2. **Sign up/Login** (free account)
3. Click your profile → **New Space**
4. Fill in details:
   - **Space name**: `ml-prediction-app` (or your choice)
   - **License**: MIT
   - **SDK**: Select **Docker**
   - **Hardware**: CPU (free tier)
5. Click **Create Space**

#### 2. Upload Files

In your new Space's **Files** tab:

```bash
# Upload these files:
✅ Dockerfile
✅ README.md
✅ app.py
✅ requirements.txt
✅ model_pruned_float16.pkl
✅ templates/ (entire folder)
✅ static/ (entire folder)
```

**Drag and drop** or use **Add file** button.

#### 3. Wait for Build

- HF automatically detects `Dockerfile` and builds
- Build takes ~3-5 minutes
- Watch logs in **App** tab
- Space will auto-start when ready! 🎉

---

### Method 2: Git Push (Advanced)

#### 1. Clone Your Space

```bash
# After creating Space on HF
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME
```

#### 2. Copy Files

```bash
# Copy all project files to the cloned directory
cp -r ../Frontend/* .
```

#### 3. Push to HF

```bash
git add .
git commit -m "Initial deployment"
git push
```

HF automatically builds and deploys!

---

## Configuration Details

### Dockerfile Explained

```dockerfile
FROM python:3.11-slim         # Lightweight Python image
WORKDIR /app                   # Working directory
COPY requirements.txt .        # Copy dependencies first (caching)
RUN pip install -r requirements.txt
COPY . .                       # Copy all files
EXPOSE 7860                    # HF Spaces uses port 7860
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:7860"]
```

### README.md Metadata

The YAML frontmatter in `README.md` configures the Space:

```yaml
---
title: ML Prediction App      # Space title
emoji: 🏥                      # Display emoji
sdk: docker                    # Use Docker SDK
---
```

---

## Accessing Your App

Once deployed, your Space URL will be:
```
https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
```

Share this link with anyone - **no authentication required**!

---

## Resource Limits (Free Tier)

| Resource | Free Tier | Notes |
|----------|-----------|-------|
| **CPU** | 2 vCPU | Sufficient for your 77MB model |
| **RAM** | 16GB | More than enough! |
| **Storage** | 50GB | Your model is only 77MB ✅ |
| **Timeout** | None | App stays running |
| **Bandwidth** | Unlimited | Free hosting forever! |

Your app will run **perfectly on the free tier**! 🎉

---

## Model Handling

Your `model_pruned_float16.pkl`:
- ✅ **77MB** - Well within limits
- ✅ Uploaded directly to Space
- ✅ Loaded from `/app/model_pruned_float16.pkl` in container
- ✅ No external storage needed

The `app.py` already handles model loading with fallback paths.

---

## Troubleshooting

### Build Fails

Check build logs in **App** tab for errors:

**Common issues:**
- Missing files → Re-upload all required files
- Python version mismatch → Dockerfile specifies 3.11
- Dependency errors → Check `requirements.txt`

### App Not Loading

1. Check if container is running: **App** tab shows status
2. View logs: Click **Logs** button
3. Port issue: Ensure `app.py` uses `PORT=7860`

### Model Not Found

Ensure file structure in Space matches:
```
/app/
  ├── Dockerfile
  ├── app.py
  ├── model_pruned_float16.pkl  ← Must be in root
  ├── requirements.txt
  ├── templates/
  └── static/
```

---

## Testing Locally with Docker

Before deploying, test Docker build locally:

```bash
# Build image
docker build -t ml-app .

# Run container
docker run -p 7860:7860 ml-app

# Visit: http://localhost:7860
```

---

## Advantages of HF Spaces

| Feature | Hugging Face Spaces | Other Platforms |
|---------|-------------------|-----------------|
| Cost | **100% FREE** | Limited free tiers |
| RAM | 16GB free | Usually <1GB |
| ML Focus | ✅ Optimized for ML | Generic hosting |
| Sharing | Public by default | Often requires auth |
| Community | ML researchers | General developers |
| Uptime | Excellent | Varies |

---

## Optional: Custom Domain

HF Spaces support custom domains (Pro plan):
- Go to Space **Settings**
- Add custom domain
- Point CNAME to HF

---

## Next Steps

### Quick Deployment (Recommended)

1. ✅ Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. ✅ Create new **Docker Space**
3. ✅ Upload all project files
4. ✅ Wait for build (~3-5 min)
5. ✅ Share your live app!

### Git-Based Deployment

1. ✅ Create Space on HF
2. ✅ Clone Space repo
3. ✅ Copy project files
4. ✅ Commit and push

---

## Your Flask App is Ready for HF Spaces! 🚀

All configuration files are in place. Just upload to Hugging Face and you're live!

**Pro tip**: After deployment, share your Space URL on:
- LinkedIn (showcase your ML project!)
- GitHub README
- Portfolio website

This is a great portfolio piece! 🌟
