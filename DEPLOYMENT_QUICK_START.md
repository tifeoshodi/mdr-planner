# 🚀 Railway Deployment - Quick Start Card

## ⚡ 5-Minute Setup Guide

### 1️⃣ Push to GitHub (2 minutes)

```bash
cd C:\Users\user\MDR_Planner
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub, then:
git remote add origin https://github.com/tifeoshodi/mdr-planner.git
git push -u origin main
```

### 2️⃣ Deploy to Railway (3 minutes)

1. **Go to** [railway.app](https://railway.app)
2. **Sign up** with GitHub
3. **New Project** → Deploy from GitHub repo
4. **Add Database** → Click "+ New" → PostgreSQL
5. **Add 3 Services:**

   **Service 1: Portfolio Manager**
   - Root Dir: `app1_portfolio_manager`
   - Start Cmd: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - Env Var: `SECRET_KEY` = [run command below]

   **Service 2: Scheduler**
   - Root Dir: `app2_scheduler`
   - Start Cmd: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - Env Var: Same `SECRET_KEY`

   **Service 3: Discipline Dashboard**
   - Root Dir: `app3_discipline_dashboard`
   - Start Cmd: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - Env Var: Same `SECRET_KEY` + `ALLOWED_EMAIL_DOMAIN=ieslglobal.com`

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3️⃣ Access Your Apps

- **Portfolio Manager:** `https://portfolio-manager-production-xxxx.up.railway.app`
- **Scheduler:** `https://scheduler-production-xxxx.up.railway.app`
- **Discipline Dashboard:** `https://discipline-dashboard-production-xxxx.up.railway.app`

**Login:**
- Email: `admin@mdr.local`
- Password: `admin123` (change immediately!)

---

## 💰 Cost

- **Free Trial:** $5 credit
- **Typical Usage:** $15-20/month
  - 3 Flask services (~$10-15)
  - PostgreSQL (~$5)

---

## 📖 Full Guide

See `DEPLOYMENT_GUIDE_RAILWAY.md` for:
- Detailed step-by-step instructions
- Troubleshooting
- Security checklist
- Backup & monitoring
- Performance optimization

---

## ✅ What's Included

- ✅ PostgreSQL database configured
- ✅ All 3 apps ready for deployment
- ✅ Production WSGI server (gunicorn)
- ✅ Environment variables template
- ✅ Railway configuration files
- ✅ Import script for real MDR data

---

## 🎯 Post-Deployment

1. **Change admin password**
2. **Import your MDR:** Upload `2506600-IESL-MDR-A-0001_B_Master...xlsx`
3. **Test all apps**
4. **Invite team members**

---

**Need Help?** Check `DEPLOYMENT_GUIDE_RAILWAY.md` for detailed instructions!
