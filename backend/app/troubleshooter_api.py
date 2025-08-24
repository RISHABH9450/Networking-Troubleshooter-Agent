"""
FastAPI endpoints for the Networking Troubleshooter web interface
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional
from pydantic import BaseModel
import json

from .networking_troubleshooter import NetworkingTroubleshooter, DiagnosticResult

router = APIRouter(prefix="/troubleshooter", tags=["networking-troubleshooter"])


class TroubleshooterConfig(BaseModel):
    frontend_port: int = 5173
    backend_port: int = 8000
    frontend_path: str = "/workspace/frontend"
    backend_path: str = "/workspace/backend"


class DiagnosticResponse(BaseModel):
    test_name: str
    status: str
    message: str
    fix_suggestion: Optional[str] = None
    commands: Optional[List[str]] = None


class TroubleshootResponse(BaseModel):
    summary: Dict[str, int]
    results: List[DiagnosticResponse]
    fix_script: Optional[str] = None


@router.post("/diagnose", response_model=TroubleshootResponse)
async def run_diagnosis(config: TroubleshooterConfig = TroubleshooterConfig()):
    """Run comprehensive networking diagnosis"""
    try:
        troubleshooter = NetworkingTroubleshooter(
            frontend_port=config.frontend_port,
            backend_port=config.backend_port,
            frontend_path=config.frontend_path,
            backend_path=config.backend_path
        )
        
        # Run diagnosis
        results = troubleshooter.run_full_diagnosis()
        
        # Convert results to response format
        diagnostic_responses = []
        for result in results:
            diagnostic_responses.append(DiagnosticResponse(
                test_name=result.test_name,
                status=result.status,
                message=result.message,
                fix_suggestion=result.fix_suggestion,
                commands=result.commands
            ))
        
        # Calculate summary
        summary = {
            "passed": sum(1 for r in results if r.status == "PASS"),
            "failed": sum(1 for r in results if r.status == "FAIL"),
            "warnings": sum(1 for r in results if r.status == "WARNING"),
            "total": len(results)
        }
        
        # Generate fix script if needed
        fix_script = None
        if summary["failed"] > 0:
            fix_script = troubleshooter.generate_fix_script(results)
        
        return TroubleshootResponse(
            summary=summary,
            results=diagnostic_responses,
            fix_script=fix_script
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagnosis failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint for troubleshooter API"""
    return {"status": "healthy", "service": "networking-troubleshooter"}


@router.get("/quick-check")
async def quick_connectivity_check():
    """Quick connectivity check without full diagnosis"""
    troubleshooter = NetworkingTroubleshooter()
    
    frontend_status = "online" if troubleshooter._is_port_accessible(5173) else "offline"
    backend_status = "online" if troubleshooter._is_port_accessible(8000) else "offline"
    
    return {
        "frontend": {
            "status": frontend_status,
            "url": "http://localhost:5173"
        },
        "backend": {
            "status": backend_status,
            "url": "http://localhost:8000"
        },
        "overall_status": "healthy" if frontend_status == "online" and backend_status == "online" else "issues_detected"
    }


@router.post("/fix-script")
async def generate_fix_script(config: TroubleshooterConfig = TroubleshooterConfig()):
    """Generate a fix script based on current issues"""
    try:
        troubleshooter = NetworkingTroubleshooter(
            frontend_port=config.frontend_port,
            backend_port=config.backend_port,
            frontend_path=config.frontend_path,
            backend_path=config.backend_path
        )
        
        results = troubleshooter.run_full_diagnosis()
        script_content = troubleshooter.generate_fix_script(results)
        
        return {
            "script": script_content,
            "filename": "fix_networking.sh",
            "issues_found": sum(1 for r in results if r.status == "FAIL")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Script generation failed: {str(e)}")


# Example usage data for the frontend
@router.get("/examples")
async def get_troubleshooting_examples():
    """Get example troubleshooting scenarios and solutions"""
    return {
        "common_issues": [
            {
                "problem": "Frontend shows 404 on /login route",
                "likely_causes": [
                    "Missing route definition in App.jsx",
                    "React Router not properly configured",
                    "Component import path incorrect"
                ],
                "quick_fixes": [
                    "Add <Route path='/login' element={<LoginPage />} /> to Routes",
                    "Verify component imports",
                    "Check for typos in route paths"
                ]
            },
            {
                "problem": "API calls fail with CORS errors",
                "likely_causes": [
                    "Backend CORS not configured",
                    "Wrong frontend origin in CORS settings",
                    "Missing preflight handling"
                ],
                "quick_fixes": [
                    "Add CORSMiddleware to FastAPI app",
                    "Include 'http://localhost:5173' in allowed origins",
                    "Enable OPTIONS method in CORS"
                ]
            },
            {
                "problem": "Tailwind styles not applying",
                "likely_causes": [
                    "Missing @tailwind directives in CSS",
                    "Incorrect content paths in tailwind.config.js",
                    "PostCSS not configured properly"
                ],
                "quick_fixes": [
                    "Add @tailwind base; @tailwind components; @tailwind utilities;",
                    "Update content paths to include all JSX/TSX files",
                    "Verify postcss.config.js has tailwindcss plugin"
                ]
            }
        ],
        "testing_commands": [
            "curl http://localhost:8000/health",
            "curl -H 'Origin: http://localhost:5173' http://localhost:8000/health",
            "npm run dev",
            "python -m uvicorn app.main:app --reload"
        ]
    }