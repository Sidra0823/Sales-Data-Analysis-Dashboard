# Deploy Sales Dashboard to Render.com

## What is Render?
Render is a free platform to deploy web apps. It's similar to Heroku but with better limits and a modern interface.

---

## 🚀 Step-by-Step Deployment Guide

### **Step 1: Create a Render Account**
1. Go to **https://render.com**
2. Click **"Sign Up"**
3. Sign up with GitHub (Sidra0823) - this makes deployment easier!
4. Authorize Render to access your GitHub account

---

### **Step 2: Create New Web Service**
1. From Render Dashboard, click **"New +"** → **"Web Service"**
2. You'll see: "Connect a repository"
3. Click **"Connect GitHub Account"** if not already done
4. Select your repository: **`Sidra0823/Sales-Data-Analysis-Dashboard`**
5. Click **"Connect"**

---

### **Step 3: Configure Deployment Settings**
Fill in the following details:

| Setting | Value |
|---------|-------|
| **Name** | `sales-dashboard` |
| **Environment** | `Docker` |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run dashboard/app.py --server.port=$PORT --server.address=0.0.0.0` |
| **Instance Type** | `Free` |

---

### **Step 4: Add Environment Variables**
Click **"Environment"** and add these variables:

```
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_LOGGER_LEVEL=info
STREAMLIT_CLIENT_SHOW_ERROR_DETAILS=false
```

---

### **Step 5: Deploy**
1. Scroll down and click **"Create Web Service"**
2. Render will automatically:
   - Build your app
   - Install dependencies
   - Deploy to live server

This takes **5-10 minutes**

---

## 📍 Your Live App URL

Once deployed, Render will give you a URL like:
```
https://sales-dashboard-xxxx.onrender.com
```

**Note:** Free tier apps sleep after 15 minutes of inactivity. Click the link to wake them up.

---

## ✅ After Deployment

### Test Your App:
1. Open your Render URL
2. Click through all dashboard tabs
3. Test filters and interactive features
4. Verify ML forecasting works

### Share Your App:
- Copy the URL and share with colleagues
- Post on portfolio/LinkedIn
- Include in project presentations

---

## 🔄 Auto-Deploy Updates

After deployment, any code push to GitHub will **automatically redeploy**:

```bash
git add .
git commit -m "Update dashboard"
git push origin main
```

Render will detect changes and redeploy automatically!

---

## 📊 What's Included in Your Deployment

✅ **Interactive KPI Dashboard**
- Total sales, transactions, growth metrics
- Customer segment analysis
- Payment method breakdown

✅ **Comprehensive Analytics**
- Daily, weekly, monthly sales trends
- Seasonal patterns
- Growth rate analysis

✅ **Product & Category Analysis**
- Top products ranking
- Category performance
- Sales distribution

✅ **Regional Intelligence**
- Sales by region
- Regional profit comparison
- Geographic breakdown

✅ **Machine Learning Forecasting**
- Sales predictions (7-90 days ahead)
- Multiple ML models (Random Forest, Gradient Boosting, Linear Regression)
- Feature importance analysis

✅ **Interactive Filters**
- Filter by date range
- Filter by category
- Filter by region
- Real-time updates

---

## 🎨 Features

- **Beautiful UI** - Professional design with custom colors
- **Interactive Charts** - Plotly visualizations
- **Responsive** - Works on desktop and mobile
- **Fast Loading** - Optimized performance
- **Real-time Updates** - Instant filtering and analysis

---

## Free Tier Limits

| Feature | Limit |
|---------|-------|
| **Apps** | Up to 3 |
| **Sleep Timeout** | 15 minutes inactivity |
| **Resources** | Shared |
| **Bandwidth** | 100 GB/month |

**Upgrade** to $7/month for:
- No auto-sleep
- Dedicated resources
- Priority support

---

## 🛠️ Troubleshooting

### **App Won't Start**
Check these in order:
1. Raw logs in Render dashboard
2. Ensure `requirements.txt` has all packages
3. Verify `dashboard/app.py` exists and is valid
4. Check environment variables are set

### **Slow Performance**
- Free tier is slower, upgrade to Pro
- Check network latency
- Reduce data size if possible

### **Port Binding Error**
Already fixed! Start command uses `$PORT` variable

---

## 📋 Project Files on Render

Your deployed app will include:
```
Sales-Dashboard/
├── dashboard/app.py           ← Main Streamlit app
├── analysis/eda.py            ← Data analysis
├── analysis/model.py          ← ML forecasting
├── data/sales_data.csv        ← Sample data
├── .streamlit/config.toml     ← Streamlit config
├── Procfile                   ← Render config
├── render.yaml                ← Render template
├── requirements.txt           ← Dependencies
└── README.md                  ← Documentation
```

---

## 🎯 Next Steps After Deployment

1. **Test All Features**
   - Browse dashboard
   - Test filtering
   - Check forecasting models

2. **Share URL**
   - LinkedIn, Twitter, GitHub
   - Portfolio website
   - Email to colleagues

3. **Monitor Performance**
   - Check Render logs
   - Track usage statistics
   - Monitor uptime

4. **Make Improvements**
   - Push updates to GitHub
   - Render auto-redeploys
   - No manual restart needed

---

## 💡 Pro Tips

✅ **Auto-Deploy with Git:**
```bash
git push origin main  # Render auto-deploys this
```

✅ **View Logs:**
- Render Dashboard → Your Service → Logs tab

✅ **Share Live URL:**
```
https://sales-dashboard-xxxx.onrender.com
```

✅ **Monitor Activity:**
- Render Dashboard shows all deployments
- Email alerts on failures
- Performance metrics available

---

## 🚀 Performance Tips

1. **For Free Tier:**
   - Keep data size reasonable
   - Close unused browser tabs
   - Refresh if app sleeps

2. **For Production:**
   - Upgrade to Pro ($7/month)
   - Use custom domain
   - Enable auto-scroll logs

---

## 🔗 Useful Links

- **Render Dashboard:** https://dashboard.render.com
- **Your GitHub Repo:** https://github.com/Sidra0823/Sales-Data-Analysis-Dashboard
- **Streamlit Docs:** https://docs.streamlit.io
- **Render Docs:** https://render.com/docs

---

## ✨ You're All Set!

Your Sales Dashboard is ready to deploy on Render. The process is completely automated:

1. ✅ Code is on GitHub
2. ✅ `render.yaml` is configured
3. ✅ `Procfile` is set up
4. ✅ `requirements.txt` is complete
5. ✅ Environment variables configured

**Just follow the steps above and your app will be live in minutes!**

