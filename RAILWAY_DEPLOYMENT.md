# Railway Deployment Guide

Complete guide to deploy your Flask ML application on Railway.

> [!IMPORTANT]
> Railway offers **$5 free credit per month** with no credit card required for the trial period. This is more generous than many other platforms.

## Prerequisites

✅ Your project already has:
- [`app.py`](file:///c:/Users/mohat/OneDrive/Desktop/Frontend/app.py) - Flask application
- [`requirements.txt`](file:///c:/Users/mohat/OneDrive/Desktop/Frontend/requirements.txt) - Python dependencies  
- [`Procfile`](file:///c:/Users/mohat/OneDrive/Desktop/Frontend/Procfile) - Start command
- [`railway.json`](file:///c:/Users/mohat/OneDrive/Desktop/Frontend/railway.json) - Railway configuration
- [`runtime.txt`](file:///c:/Users/mohat/OneDrive/Desktop/Frontend/runtime.txt) - Python version
- `model_pruned_float16.pkl` - ML model (77MB - perfectly fine for Railway!)

---

## Deployment Steps

### 1. Push Code to GitHub

```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 2. Deploy on Railway

1. **Go to** [Railway.app](https://railway.app/)
2. **Sign up/Login** with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your repository
6. Railway will **auto-detect** your Flask app!

### 3. Configuration (Auto-detected)

Railway automatically detects:
- ✅ Python runtime from `runtime.txt`
- ✅ Dependencies from `requirements.txt`  
- ✅ Start command from `Procfile`
- ✅ Port from environment variable

**No manual configuration needed!**

### 4. Environment Variables

Railway auto-generates `PORT` - no setup required.

If you need custom variables:
- Go to your project → **Variables** tab
- Add any custom environment variables

### 5. Get Your URL

Once deployed:
- Railway provides a URL like: `https://your-app.up.railway.app`
- Click **"Generate Domain"** in the Settings tab
- Your app is live! 🚀

---

## Model Handling

Your `model_pruned_float16.pkl` (77MB) will be deployed with the app:
- ✅ **No file size limits** on Railway
- ✅ Model loads from local path automatically
- ✅ No external storage needed

---

## Monitoring & Logs

Railway provides:
- **Real-time logs** - See application output
- **Metrics** - CPU, Memory, Network usage
- **Auto-restart** - Configured in `railway.json`

Access logs: Project Dashboard → **Deployments** → Click deployment → **View Logs**

---

## Troubleshooting

### Build Fails
Check build logs for missing dependencies:
```bash
# Logs will show which package failed
# Update requirements.txt if needed
```

### App Crashes on Startup
Common issues:
- **Port binding**: Ensure `app.py` uses `PORT` from environment
  ```python
  port = int(os.environ.get("PORT", 10000))
  ```
- **Model loading**: Check logs for model path errors

### Memory Issues
Free tier has sufficient memory for your 77MB model. If needed:
- Upgrade to **Hobby plan** ($5/month) for more resources

---

## Cost Breakdown

| Tier | Price | Resources |
|------|-------|-----------|
| Trial | **$5 credit/month** | 512MB RAM, Shared CPU |
| Hobby | **$5/month** | 512MB RAM, Shared CPU |
| Pro | **$20/month** | 8GB RAM, 8 vCPUs |

Your app should work perfectly on the **free trial**!

---

## Local Testing

Test your production configuration locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Windows: Use waitress instead of gunicorn
pip install waitress
waitress-serve --port=10000 app:app

# Linux/Mac: Use gunicorn
gunicorn app:app --workers 1 --threads 2 --timeout 120
```

Visit: `http://localhost:10000`

---

## Advantages Over Render

| Feature | Railway | Render |
|---------|---------|--------|
| Free Credit | $5/month | Limited hours |
| Build Time | Faster | Slower on free tier |
| Dashboard | Modern UI | Functional |
| Auto-deploy | ✅ Yes | ✅ Yes |
| Custom Domains | ✅ Free | ✅ Free |

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Sign up on Railway.app
3. ✅ Deploy from GitHub repo
4. ✅ Generate domain
5. ✅ Test your live app!

**Your project is ready to deploy!** 🎉
