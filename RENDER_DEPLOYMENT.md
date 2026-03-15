# Deploying ReThread to Render

## Quick Start

1. **Push to GitHub** (if not already done)
   ```bash
   git add -A
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

2. **Create Render Service**
   - Go to [render.com](https://render.com)
   - Click "New+" → "Web Service"
   - Connect your GitHub repository
   - Select the ReThread repository
   - Environment: Python 3.10
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -c gunicorn_config.py app:app`
   - Click "Create Web Service"

3. **Set Environment Variables** (CRITICAL)
   - In Render dashboard: Settings → Environment
   - Add new environment variable:
     - Key: `ANTHROPIC_API_KEY`
     - Value: `sk-ant-api03-YOUR_ACTUAL_KEY`
   - Also add:
     - Key: `FLASK_ENV`
     - Value: `production`

4. **Check Deployment**
   - Render will automatically build and deploy
   - Check logs for errors
   - Once green ("Live"), your app is running
   - URL will be something like: `https://rethread-123.onrender.com`

## Troubleshooting

**App crashes on startup:**
- Check Environment Variables (especially ANTHROPIC_API_KEY)
- Check Build Logs in Render dashboard
- Look for Python errors

**API endpoints not responding:**
- Verify PORT environment variable is picked up
- Check if Gunicorn is running correctly in logs
- Ensure .env variables are set in Render (not just locally)

**Frontend can't reach API:**
- Update frontend to use the new Render URL
- Check CORS if frontend is on different domain
- Verify API endpoints are accessible at `https://rethread-xxx.onrender.com/analyze`

## Files Added for Render

- `Procfile` - Tells Render how to start the app
- `render.yaml` - Render configuration (optional, for Infrastructure as Code)
- `gunicorn_config.py` - Production WSGI server configuration

## Environment Variables Used

| Variable | Value | Where to Set |
|----------|-------|--------------|
| ANTHROPIC_API_KEY | Your API key | Render dashboard |
| FLASK_ENV | production | render.yaml (auto) |
| PORT | Dynamic (assigned by Render) | Auto-detected |

## Post-Deployment

1. Test a material analysis:
   ```bash
   curl -X POST https://rethread-xxx.onrender.com/analyze \
     -H "Content-Type: application/json" \
     -d '{"material": "cotton"}'
   ```

2. Check available materials:
   ```bash
   curl https://rethread-xxx.onrender.com/materials
   ```

3. Monitor logs in Render dashboard (Settings → Logs)

## Important Security Notes

- ✅ API key is NOT in code (only in Render environment)
- ✅ Debug mode is OFF in production
- ✅ API key print statement removed from logs
- ✅ .env file is in .gitignore (won't be committed)
- ✅ Gunicorn handles concurrent requests properly

Happy deploying! 🚀
