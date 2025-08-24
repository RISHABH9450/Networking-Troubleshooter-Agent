# 🔧 AgentHack 2025 Troubleshooter Demo

## Example Scenario: "Frontend loads but API calls fail with CORS errors"

### 1. Problem Description
```
User reports:
- Frontend is running at http://localhost:5173  
- Backend is running at http://localhost:5000
- React shows a 404 page when navigating to /login
- Tailwind styles are not applying
- API calls to /tasks fail with CORS errors
```

### 2. Running the Troubleshooter

```bash
# Quick CLI diagnosis
python3 troubleshoot.py

# Or using the web interface
# Visit: http://localhost:5173/agenthack
```

### 3. Expected Output

```
🔍 Starting AgentHack 2025 Networking Diagnosis...
============================================================

🌐 Step 1: Frontend-Backend Connectivity
----------------------------------------
✅ Frontend Server: Frontend is running on http://localhost:5173
❌ Backend Server: Backend not accessible on http://localhost:8000
💡 Fix: Check if backend is running on port 5000 instead of 8000

🛣️ Step 2: Route and 404 Issues  
----------------------------------------
✅ React Router Setup: React Router is configured in App.jsx
❌ Route Coverage: /login route not found in routing configuration
💡 Fix: Add <Route path="/login" element={<LoginPage />} /> to Routes

🎨 Step 3: Tailwind CSS Integration
----------------------------------------
❌ Tailwind CSS Import: Tailwind directives not found in CSS files
💡 Fix: Add @tailwind base; @tailwind components; @tailwind utilities;

🔌 Step 4: API Communication
----------------------------------------
⚠️ Environment Variables: No .env file found
💡 Fix: Create .env with VITE_API_URL=http://localhost:5000

🔐 Step 5: CORS Configuration
----------------------------------------
❌ CORS Configuration: No CORS configuration found in backend
💡 Fix: Add CORSMiddleware to FastAPI app

============================================================
📋 DIAGNOSTIC SUMMARY
============================================================
✅ Passed: 3
❌ Failed: 4  
⚠️ Warnings: 2
```

### 4. Step-by-Step Fix Process

#### Fix 1: Update Backend Port Configuration
```python
# In troubleshooter dashboard, change backend port from 8000 to 5000
# Or update backend to run on port 8000:
uvicorn app.main:app --reload --port 8000
```

#### Fix 2: Add Missing Route
```jsx
// In src/App.jsx, add to Routes:
<Route path="/login" element={<LoginPage />} />
```

#### Fix 3: Add Tailwind Directives
```css
/* In src/index.css or styles/tailwind.css */
@tailwind base;
@tailwind components;  
@tailwind utilities;
```

#### Fix 4: Create Environment File
```bash
# Create frontend/.env
VITE_API_URL=http://localhost:5000
```

#### Fix 5: Add CORS Configuration
```python
# In backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 5. Verification

```bash
# Run troubleshooter again to verify fixes
python3 troubleshoot.py

# Expected result:
# ✅ Passed: 10
# ❌ Failed: 0
# ⚠️ Warnings: 0
```

### 6. Generated Fix Script

The troubleshooter automatically generates `fix_networking.sh`:

```bash
#!/bin/bash

# AgentHack 2025 Networking Fix Script

# Fix: Backend Server
cd backend
python -m uvicorn app.main:app --reload --port 8000

# Fix: Route Coverage  
# Add <Route path="/login" element={<LoginPage />} /> to Routes

# Fix: Tailwind CSS Import
# Add @tailwind base; @tailwind components; @tailwind utilities; to CSS

# Fix: Environment Variables
echo "VITE_API_URL=http://localhost:8000" > ../frontend/.env

# Fix: CORS Configuration
# Add CORSMiddleware to FastAPI app with allowed origins
```

### 7. Web Interface Features

When using the web interface at `/agenthack`:

- **🚀 Quick Status Check**: Shows frontend/backend status at a glance
- **⚙️ Configuration Panel**: Adjust ports and paths 
- **🔍 Full Diagnosis**: Comprehensive testing with detailed results
- **📥 Download Fix Script**: Get automated fix commands
- **📊 Visual Summary**: Color-coded test results with statistics

### 8. Common Resolution Patterns

| Issue Type | Detection | Auto-Fix Available |
|------------|-----------|-------------------|
| Port Conflicts | ✅ | ✅ |
| Missing Routes | ✅ | ⚠️ Manual |
| CORS Errors | ✅ | ⚠️ Template |
| Tailwind Setup | ✅ | ✅ |
| API Configuration | ✅ | ✅ |
| Environment Variables | ✅ | ✅ |

### 9. Integration with Development Workflow

```bash
# Add to package.json scripts:
{
  "scripts": {
    "troubleshoot": "python3 ../troubleshoot.py",
    "fix": "bash ../fix_networking.sh"
  }
}

# Usage:
npm run troubleshoot
npm run fix
```

This comprehensive troubleshooter saves developers hours of debugging time by automatically detecting and providing fixes for the most common frontend-backend integration issues in React + Vite + Python applications.