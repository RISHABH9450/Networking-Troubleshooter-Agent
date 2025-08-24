# 🔧 AgentHack 2025 Networking Troubleshooter

A comprehensive tool to debug frontend-backend connectivity issues in React + Vite + Python (FastAPI) applications.

## 🚀 Quick Start

### Option 1: Command Line Interface

```bash
# Quick diagnosis
python troubleshoot.py

# Or use the full module
python -m backend.app.networking_troubleshooter
```

### Option 2: Web Interface

1. Start the backend server:
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```

3. Navigate to `http://localhost:5173/agenthack`

## 🔍 What It Diagnoses

### 1. Frontend-Backend Connectivity
- ✅ Checks if frontend (localhost:5173) is accessible
- ✅ Checks if backend (localhost:8000) is accessible  
- ✅ Detects port conflicts and suggests alternatives
- ✅ Tests actual HTTP connectivity between services

### 2. Route and 404 Issues
- ✅ Verifies React Router setup in App.jsx
- ✅ Checks for common routes (/login, /dashboard, /tasks)
- ✅ Validates index.html entry point
- ✅ Detects missing route configurations

### 3. Tailwind CSS Integration
- ✅ Validates tailwind.config.js content paths
- ✅ Checks PostCSS configuration
- ✅ Verifies @tailwind directives in CSS files
- ✅ Ensures proper build chain integration

### 4. API Communication
- ✅ Checks for API service files (services/api.js)
- ✅ Validates environment variable configuration
- ✅ Tests backend health endpoint
- ✅ Detects incorrect base URL configurations

### 5. CORS Configuration
- ✅ Verifies CORS middleware in backend
- ✅ Checks allowed origins for local development
- ✅ Tests preflight request handling
- ✅ Provides FastAPI and Flask specific guidance

## 🛠️ Example Usage Scenarios

### Scenario 1: Frontend 404 on /login
```
Problem: "React app shows 404 when navigating to /login"

Diagnosis:
❌ React Router Setup: Missing route definition
💡 Fix: Add <Route path="/login" element={<LoginPage />} /> to Routes

Commands:
- Verify component imports
- Check for typos in route paths
```

### Scenario 2: CORS Errors on API Calls
```
Problem: "API calls fail with CORS policy errors"

Diagnosis:
❌ CORS Configuration: No CORS middleware found in backend
💡 Fix: Add CORS middleware to backend

Commands:
- from fastapi.middleware.cors import CORSMiddleware
- app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173'])
```

### Scenario 3: Tailwind Styles Not Applying
```
Problem: "Tailwind classes don't work in components"

Diagnosis:
❌ Tailwind Content Paths: Incorrect content paths in config
💡 Fix: Update content paths in tailwind.config.js

Commands:
- Set content: ["./src/**/*.{js,jsx,ts,tsx}", "./index.html"]
```

## 📋 Output Format

Each diagnostic test returns:

```json
{
  "test_name": "CORS Configuration",
  "status": "FAIL",  // PASS, FAIL, WARNING
  "message": "No CORS configuration found in backend",
  "fix_suggestion": "Add CORS middleware to backend",
  "commands": [
    "from fastapi.middleware.cors import CORSMiddleware",
    "app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173'])"
  ]
}
```

## 🔧 Auto-Fix Script Generation

The troubleshooter automatically generates bash scripts to fix common issues:

```bash
# Generated fix script example
#!/bin/bash

# Fix: Frontend Server
cd frontend
npm run dev

# Fix: CORS Configuration  
# Add CORSMiddleware to FastAPI app

# Fix: Tailwind Content Paths
# Set content: ["./src/**/*.{js,jsx,ts,tsx}", "./index.html"]
```

## 🌐 API Endpoints

### REST API (Backend)

```bash
# Quick connectivity check
GET /troubleshooter/quick-check

# Full diagnosis
POST /troubleshooter/diagnose
{
  "frontend_port": 5173,
  "backend_port": 8000,
  "frontend_path": "/workspace/frontend",
  "backend_path": "/workspace/backend"
}

# Generate fix script
POST /troubleshooter/fix-script

# Get troubleshooting examples
GET /troubleshooter/examples

# Health check
GET /troubleshooter/health
```

## 🎯 Common Issues & Solutions

### Issue: "Cannot connect to backend"
**Symptoms:** Frontend loads but API calls fail
**Solution:** 
1. Check if backend server is running
2. Verify CORS configuration
3. Check firewall/port blocking

### Issue: "Page not found (404)"
**Symptoms:** Direct URL navigation fails in React app
**Solution:**
1. Add React Router configuration
2. Verify route definitions in App.jsx
3. Check for missing components

### Issue: "Styles not loading"
**Symptoms:** Tailwind classes have no effect
**Solution:**
1. Check @tailwind directives in CSS
2. Verify tailwind.config.js content paths
3. Restart dev server after config changes

### Issue: "API base URL incorrect"
**Symptoms:** Network errors on API calls
**Solution:**
1. Create .env file with VITE_API_URL
2. Update axios configuration
3. Use environment variables in API service

## 🔄 Continuous Monitoring

For development environments, you can run the troubleshooter periodically:

```bash
# Check status every 30 seconds
while true; do
  python troubleshoot.py
  sleep 30
done
```

## 🚨 Emergency Troubleshooting

If all else fails, try this reset sequence:

```bash
# 1. Stop all servers
pkill -f "npm"
pkill -f "uvicorn"

# 2. Clear caches
cd frontend
rm -rf node_modules/.cache
rm -rf dist/

# 3. Restart everything
npm run dev &
cd ../backend
python -m uvicorn app.main:app --reload --port 8000 &

# 4. Run diagnosis
python ../troubleshoot.py
```

## 🤝 Contributing

To extend the troubleshooter:

1. Add new diagnostic methods to `NetworkingTroubleshooter` class
2. Update the web interface in `TroubleshooterDashboard.jsx`
3. Add new API endpoints in `troubleshooter_api.py`
4. Update this documentation

## 📞 Support

For issues with the troubleshooter itself:
1. Check the console logs
2. Verify Python dependencies in requirements.txt
3. Ensure React dependencies in package.json
4. Test the individual diagnostic components

---

**Happy debugging! 🎉**
