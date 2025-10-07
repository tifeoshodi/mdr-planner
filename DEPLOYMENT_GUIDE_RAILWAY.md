# MDR System - Railway Deployment Guide

## 🚀 Complete Step-by-Step Deployment Guide

This guide will walk you through deploying all 3 MDR applications to Railway.app with a shared PostgreSQL database.

---

## 📋 Prerequisites

### 1. Create Accounts
- ✅ **GitHub Account** - [github.com](https://github.com)
- ✅ **Railway Account** - [railway.app](https://railway.app) (sign up with GitHub)

### 2. Install Git (if not already installed)
```bash
# Check if Git is installed
git --version

# If not installed, download from: https://git-scm.com/downloads
```

---

## 📦 Part 1: Prepare Your Repository

### Step 1: Initialize Git Repository

```bash
# Navigate to your project directory
cd C:\Users\user\MDR_Planner

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - MDR System ready for deployment"
```

### Step 2: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click "New Repository" (green button)
3. Repository name: `mdr-planner` (or your preferred name)
4. Description: "Master Document Register Management System"
5. **Important:** Keep it **PRIVATE** (contains business logic)
6. **Don't** initialize with README (we already have one)
7. Click "Create Repository"

### Step 3: Push to GitHub

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/mdr-planner.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🚂 Part 2: Deploy to Railway

### Step 1: Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access your GitHub
5. Select your `mdr-planner` repository
6. Railway will detect it's a Python project

### Step 2: Add PostgreSQL Database

1. In your Railway project dashboard
2. Click "+ New" → "Database" → "Add PostgreSQL"
3. Railway will automatically:
   - Create a PostgreSQL instance
   - Set `DATABASE_URL` environment variable
   - Connect it to all your services

### Step 3: Create Service for Portfolio Manager (App 1)

1. Click "+ New" → "GitHub Repo" → Select your repo
2. Name the service: `portfolio-manager`
3. Click "Settings" tab
4. **Root Directory:** Set to `app1_portfolio_manager`
5. **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
6. **Environment Variables:**
   - Click "Variables" tab
   - Add: `SECRET_KEY` = `[generate random key - see below]`
   - Railway automatically adds `DATABASE_URL` and `PORT`

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 4: Create Service for Scheduler (App 2)

1. Click "+ New" → "GitHub Repo" → Select your repo
2. Name the service: `scheduler`
3. Click "Settings" tab
4. **Root Directory:** Set to `app2_scheduler`
5. **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
6. **Environment Variables:**
   - Add the same `SECRET_KEY` as App 1

### Step 5: Create Service for Discipline Dashboard (App 3)

1. Click "+ New" → "GitHub Repo" → Select your repo
2. Name the service: `discipline-dashboard`
3. Click "Settings" tab
4. **Root Directory:** Set to `app3_discipline_dashboard`
5. **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
6. **Environment Variables:**
   - Add the same `SECRET_KEY` as App 1
   - Add: `ALLOWED_EMAIL_DOMAIN` = `ieslglobal.com`

---

## 🌐 Part 3: Configure Public URLs

### Step 1: Get Your URLs

After deployment, each service will have a public URL:

1. **Portfolio Manager:** `https://portfolio-manager-production-xxxx.up.railway.app`
2. **Scheduler:** `https://scheduler-production-xxxx.up.railway.app`
3. **Discipline Dashboard:** `https://discipline-dashboard-production-xxxx.up.railway.app`

### Step 2: (Optional) Add Custom Domains

1. Click on a service → "Settings" tab
2. Scroll to "Domains"
3. Click "Generate Domain" for a custom Railway subdomain
4. Or add your own domain (requires DNS configuration)

Examples:
- `mdr-dcc.up.railway.app`
- `mdr-scheduler.up.railway.app`
- `mdr-disciplines.up.railway.app`

---

## 🔧 Part 4: Initial Setup & Testing

### Step 1: Access Portfolio Manager

1. Open your Portfolio Manager URL
2. You should see the login page
3. Default admin login:
   - Email: `admin@mdr.local`
   - Password: `admin123`
4. **IMPORTANT:** Change this password immediately!

### Step 2: Import Your Real MDR Data

1. Login to Portfolio Manager
2. Click "Import MDR from Excel"
3. Upload: `2506600-IESL-MDR-A-0001_B_Master Deliverables Register and Progress Measurement System.xlsx`
4. Your 179 documents will be imported into PostgreSQL!

### Step 3: Test All Applications

**Portfolio Manager:**
- ✅ View portfolios
- ✅ Use spreadsheet view
- ✅ Export to Excel
- ✅ Post client feedback

**Scheduler:**
- ✅ View portfolios
- ✅ Manage disciplines
- ✅ Invite users
- ✅ Create WBS

**Discipline Dashboard:**
- ✅ Register new user (with @ieslglobal.com email)
- ✅ View dashboard
- ✅ Submit documents
- ✅ View client feedback

---

## 📊 Part 5: Monitoring & Maintenance

### View Logs

Each service has logs accessible via:
1. Click on service
2. Click "Deployments" tab
3. Click on latest deployment
4. View build and runtime logs

### Monitor Database

1. Click on PostgreSQL service
2. View "Metrics" tab for:
   - Connection count
   - Database size
   - Query performance

### Redeploy Services

If you make changes:
```bash
# Make your changes locally
git add .
git commit -m "Description of changes"
git push

# Railway automatically redeploys!
```

---

## 💰 Cost Estimation

### Railway Pricing (as of 2024)

**Free Trial:**
- $5 in credits (no credit card required)
- Good for testing and development

**Hobby Plan ($5/month):**
- $5 credit per month
- Pay for usage beyond credits
- Typical cost for your setup:
  - 3 Flask services: ~$10-15/month
  - PostgreSQL: ~$5/month
  - **Total: ~$15-20/month**

**Pro Plan ($20/month):**
- More resources
- Better performance
- Team collaboration

### Cost Optimization Tips

1. **Use 1 worker per service** (instead of 2)
   - Update Procfile: `--workers 1`
   - Saves 30-40% on costs

2. **Combine services** (if traffic is low)
   - Merge App 2 (Scheduler) into App 1
   - Reduces to 2 services

3. **Use hobby PostgreSQL** (10 GB limit)
   - Sufficient for ~50,000 documents

---

## 🔒 Security Checklist

### Before Going Live

- [ ] Change default admin password
- [ ] Set strong `SECRET_KEY` for each app
- [ ] Enable HTTPS (automatic on Railway)
- [ ] Configure allowed email domain
- [ ] Set up database backups (Railway auto-backups)
- [ ] Review file upload limits
- [ ] Add team members to Railway project
- [ ] Configure environment-specific settings

### Ongoing Security

- [ ] Regular database backups (Railway provides these)
- [ ] Monitor logs for suspicious activity
- [ ] Keep dependencies updated
- [ ] Rotate SECRET_KEY periodically
- [ ] Audit user access regularly

---

## 🐛 Troubleshooting

### Service Won't Start

**Check logs:**
1. Go to service → Deployments → View logs
2. Common issues:
   - Missing environment variables
   - Database connection errors
   - Python dependency conflicts

**Solution:**
```bash
# Make sure all environment variables are set
# Check that DATABASE_URL is present (added by PostgreSQL plugin)
# Verify SECRET_KEY is set for each service
```

### Database Connection Errors

**Error:** `could not connect to server`

**Solution:**
1. Verify PostgreSQL service is running
2. Check that services are linked to database
3. In Railway: Service → Settings → Connect to PostgreSQL

### Import Errors

**Error:** `No module named 'psycopg2'`

**Solution:**
```bash
# Ensure psycopg2-binary is in requirements_flask_apps.txt
# Trigger redeploy by pushing a change
```

### Port Binding Errors

**Error:** `Address already in use`

**Solution:**
- Railway sets `PORT` environment variable automatically
- Gunicorn uses `$PORT` from Procfile
- Don't hardcode port 5001, 5002, 5003 in production

### Upload Folder Errors

**Error:** `FileNotFoundError: uploads/`

**Solution:**
1. Railway's filesystem is ephemeral
2. For production, consider:
   - AWS S3 for file storage
   - Railway's persistent volumes (paid feature)
3. For now, uploads work but may be lost on redeploy

---

## 📈 Performance Optimization

### Database Indexing

```python
# Already optimized in models.py
# Key indexes on:
# - portfolio_id
# - discipline_id
# - doc_number
```

### Caching (Future Enhancement)

```python
# Add Redis for session storage
# Railway has Redis plugin
```

### CDN for Static Files (Future)

```python
# Use Railway's CDN or Cloudflare
# For serving Excel files, images
```

---

## 🔄 Backup & Recovery

### Automatic Backups (Railway)

Railway automatically backs up PostgreSQL:
- Daily snapshots
- 7-day retention on Hobby plan
- 30-day retention on Pro plan

### Manual Backup

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Backup database
railway run pg_dump > backup_$(date +%Y%m%d).sql
```

### Restore from Backup

```bash
# Restore to Railway database
railway run psql < backup_20241007.sql
```

---

## 📚 Additional Resources

### Railway Documentation
- [Railway Docs](https://docs.railway.app)
- [PostgreSQL Plugin](https://docs.railway.app/databases/postgresql)
- [Environment Variables](https://docs.railway.app/develop/variables)

### Flask Production Best Practices
- [Flask Deployment](https://flask.palletsprojects.com/en/3.0.x/deploying/)
- [Gunicorn Docs](https://docs.gunicorn.org/)
- [PostgreSQL with SQLAlchemy](https://docs.sqlalchemy.org/en/20/)

### Your MDR System Docs
- `README.md` - System overview
- `QUICK_START_GUIDE.md` - Local development
- `SYSTEM_OVERVIEW.md` - Architecture details
- `REAL_MDR_TEST_REPORT.md` - Testing results

---

## ✅ Deployment Checklist

### Pre-Deployment
- [x] Database updated to support PostgreSQL
- [x] Requirements updated with psycopg2-binary
- [x] Procfiles created for all 3 apps
- [x] Railway configuration files created
- [x] .gitignore configured
- [ ] Git repository initialized
- [ ] Code pushed to GitHub

### Railway Setup
- [ ] Railway account created
- [ ] GitHub connected to Railway
- [ ] Project created
- [ ] PostgreSQL database added
- [ ] Portfolio Manager service deployed
- [ ] Scheduler service deployed
- [ ] Discipline Dashboard service deployed
- [ ] Environment variables configured
- [ ] Public URLs tested

### Post-Deployment
- [ ] Admin password changed
- [ ] Real MDR data imported
- [ ] All 3 apps tested
- [ ] Team members invited
- [ ] Documentation shared with team
- [ ] Monitoring set up
- [ ] Backup strategy confirmed

---

## 🎉 Success!

Once all checkboxes are complete, your MDR System is live on Railway!

**Your Team Can Now:**
- Access from anywhere with internet
- Collaborate in real-time
- Upload/download documents
- Track project progress
- Generate MDR reports

**Next Steps:**
1. Train your team on the system
2. Import all project MDRs
3. Configure email notifications (future feature)
4. Set up regular backups
5. Monitor usage and performance

---

## 💡 Need Help?

### Railway Support
- Discord: [railway.app/discord](https://discord.gg/railway)
- Email: team@railway.app
- Docs: docs.railway.app

### MDR System Support
- Check logs in Railway dashboard
- Review `SYSTEM_OVERVIEW.md` for architecture
- Review `REAL_MDR_TEST_REPORT.md` for test results

---

**Estimated Time for Deployment: 30-45 minutes**

**Difficulty Level: Intermediate** (with this guide: Easy!)

Good luck with your deployment! 🚀
