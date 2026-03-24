# Deploy ReScript API to Render

**Time:** 5 minutes  
**Cost:** Free tier (starter plan)

---

## Step 1: Go to Render
1. Open https://render.com
2. Sign in with GitHub (recommended) or email

---

## Step 2: Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Choose deployment method:

**Option A: Connect GitHub Repo** (recommended)
- Click "Connect repository"
- Select your GitHub account
- Find/select the repo with ReScript-API folder
- Click "Connect"

**Option B: Deploy from Git URL**
- Paste: `https://github.com/yourusername/ReScript-API.git`
- Click "Continue"

**Option C: Upload Files** (if no Git)
- Download this folder as ZIP
- Upload to Render dashboard

---

## Step 3: Configure Service
Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | `rescript-api` |
| **Region** | Oregon (closest to you) |
| **Branch** | `main` (or master) |
| **Root Directory** | `ReScript-API` (if folder is in repo root, leave blank) |
| **Runtime** | `Python 3` |
| **Plan** | `Starter` (free) |

---

## Step 4: Build & Start Commands
**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Step 5: Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**:

| Key | Value |
|-----|-------|
| `DEEPGRAM_API_KEY` | `0b45d86683f50c93301257790761a1c33128b775` |
| `PYTHON_VERSION` | `3.12.0` |

---

## Step 6: Deploy
1. Click **"Create Web Service"**
2. Wait 2-3 minutes for build/deploy
3. You'll get a URL like: `https://rescript-api-xxxx.onrender.com`
4. Test: `https://rescript-api-xxxx.onrender.com/health`

---

## Step 7: Connect to Base44
Once deployed, give me the Render URL and I'll:
1. Update Base44 ReScript to call the API
2. Test full flow (URL → transcript → rewrite → merge)
3. Add subscription pricing
4. Forward rescript.ca domain

---

## Health Check
Test your deployed API:
```
GET https://rescript-api-xxxx.onrender.com/health
Response: {"status": "ok", "service": "rescript-api"}
```

## Test Transcription
```
POST https://rescript-api-xxxx.onrender.com/transcribe
Body: {"video_url": "https://www.facebook.com/reel/952209190562964"}
```

---

**Done!** Paste the Render URL here when ready.
