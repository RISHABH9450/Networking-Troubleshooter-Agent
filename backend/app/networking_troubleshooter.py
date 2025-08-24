"""
Networking Troubleshooter Agent for AgentHack 2025
A comprehensive tool to debug frontend-backend connectivity issues
"""

import os
import json
import requests
import subprocess
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class DiagnosticResult:
    """Container for diagnostic test results"""
    test_name: str
    status: str  # "PASS", "FAIL", "WARNING"
    message: str
    fix_suggestion: Optional[str] = None
    commands: Optional[List[str]] = None


class NetworkingTroubleshooter:
    """Comprehensive networking troubleshooter for React + Vite + Python backend"""
    
    def __init__(self, frontend_port: int = 5173, backend_port: int = 8000, 
                 frontend_path: str = "/workspace/frontend", backend_path: str = "/workspace/backend"):
        self.frontend_port = frontend_port
        self.backend_port = backend_port
        self.frontend_path = Path(frontend_path)
        self.backend_path = Path(backend_path)
        self.frontend_url = f"http://localhost:{frontend_port}"
        self.backend_url = f"http://localhost:{backend_port}"
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def run_full_diagnosis(self) -> List[DiagnosticResult]:
        """Run comprehensive networking diagnosis"""
        results = []
        
        print("🔍 Starting AgentHack 2025 Networking Diagnosis...")
        print("=" * 60)
        
        # Step 1: Frontend-Backend Connectivity
        results.extend(self._check_connectivity())
        
        # Step 2: Route and 404 Issues
        results.extend(self._check_routes())
        
        # Step 3: Tailwind CSS Integration
        results.extend(self._check_tailwind())
        
        # Step 4: API Communication
        results.extend(self._check_api_communication())
        
        # Step 5: CORS Configuration
        results.extend(self._check_cors_configuration())
        
        return results
    
    def _check_connectivity(self) -> List[DiagnosticResult]:
        """Check basic frontend-backend connectivity"""
        results = []
        
        print("\n🌐 Step 1: Frontend-Backend Connectivity")
        print("-" * 40)
        
        # Check if ports are available
        frontend_running = self._is_port_accessible(self.frontend_port)
        backend_running = self._is_port_accessible(self.backend_port)
        
        if frontend_running:
            results.append(DiagnosticResult(
                "Frontend Server", "PASS", 
                f"Frontend is running on {self.frontend_url}",
                None
            ))
        else:
            results.append(DiagnosticResult(
                "Frontend Server", "FAIL",
                f"Frontend not accessible on {self.frontend_url}",
                "Start the frontend development server",
                ["cd frontend", "npm run dev"]
            ))
        
        if backend_running:
            results.append(DiagnosticResult(
                "Backend Server", "PASS",
                f"Backend is running on {self.backend_url}",
                None
            ))
        else:
            results.append(DiagnosticResult(
                "Backend Server", "FAIL",
                f"Backend not accessible on {self.backend_url}",
                "Start the backend server",
                ["cd backend", "python -m uvicorn app.main:app --reload --port 8000"]
            ))
        
        # Check for port conflicts
        if not frontend_running:
            alternative_ports = self._find_alternative_ports([3000, 3001, 5174, 8080])
            if alternative_ports:
                results.append(DiagnosticResult(
                    "Port Conflict Check", "WARNING",
                    f"Frontend port {self.frontend_port} may be in use. Alternative ports available: {alternative_ports}",
                    "Try using an alternative port",
                    [f"vite --port {alternative_ports[0]}"]
                ))
        
        return results
    
    def _check_routes(self) -> List[DiagnosticResult]:
        """Check for routing and 404 issues"""
        results = []
        
        print("\n🛣️  Step 2: Route and 404 Issues")
        print("-" * 40)
        
        # Check App.jsx for routing configuration
        app_jsx_path = self.frontend_path / "src" / "App.jsx"
        if app_jsx_path.exists():
            with open(app_jsx_path, 'r') as f:
                app_content = f.read()
            
            # Check for React Router setup
            if "react-router-dom" in app_content or "BrowserRouter" in app_content:
                results.append(DiagnosticResult(
                    "React Router Setup", "PASS",
                    "React Router is configured in App.jsx",
                    None
                ))
                
                # Check for common routes
                common_routes = ["/login", "/dashboard", "/tasks", "/home"]
                missing_routes = []
                for route in common_routes:
                    if route not in app_content:
                        missing_routes.append(route)
                
                if missing_routes:
                    results.append(DiagnosticResult(
                        "Route Coverage", "WARNING",
                        f"Common routes not found: {missing_routes}",
                        "Add missing routes to your routing configuration",
                        ['Add <Route path="/login" element={<LoginPage />} /> to your Routes']
                    ))
            else:
                results.append(DiagnosticResult(
                    "React Router Setup", "FAIL",
                    "React Router not properly configured",
                    "Set up React Router in App.jsx",
                    ["npm install react-router-dom", "Import BrowserRouter, Routes, Route from react-router-dom"]
                ))
        else:
            results.append(DiagnosticResult(
                "App.jsx File", "FAIL",
                "App.jsx not found in src directory",
                "Create App.jsx with proper routing setup",
                ["Create src/App.jsx with React Router configuration"]
            ))
        
        # Check index.html
        index_html_path = self.frontend_path / "index.html"
        if index_html_path.exists():
            results.append(DiagnosticResult(
                "Entry Point", "PASS",
                "index.html found",
                None
            ))
        else:
            results.append(DiagnosticResult(
                "Entry Point", "FAIL",
                "index.html not found",
                "Create index.html in the frontend root",
                ["Create index.html with proper React app structure"]
            ))
        
        return results
    
    def _check_tailwind(self) -> List[DiagnosticResult]:
        """Check Tailwind CSS configuration and integration"""
        results = []
        
        print("\n🎨 Step 3: Tailwind CSS Integration")
        print("-" * 40)
        
        # Check tailwind.config.js
        tailwind_config_path = self.frontend_path / "tailwind.config.js"
        if tailwind_config_path.exists():
            with open(tailwind_config_path, 'r') as f:
                tailwind_content = f.read()
            
            # Check content paths (more flexible pattern matching)
            has_content = "content:" in tailwind_content
            has_src_glob = ("./src/**/*.{js,jsx}" in tailwind_content or 
                           "./src/**/*.{ts,tsx}" in tailwind_content or
                           "./src/**/*.{js,jsx,ts,tsx}" in tailwind_content)
            has_index = "./index.html" in tailwind_content or '"./index.html"' in tailwind_content
            
            if has_content and has_src_glob:
                results.append(DiagnosticResult(
                    "Tailwind Content Paths", "PASS",
                    "Tailwind content paths are properly configured",
                    None
                ))
            else:
                results.append(DiagnosticResult(
                    "Tailwind Content Paths", "FAIL",
                    "Tailwind content paths not properly configured",
                    "Update content paths in tailwind.config.js",
                    ['Set content: ["./src/**/*.{js,jsx,ts,tsx}", "./index.html"]']
                ))
        else:
            results.append(DiagnosticResult(
                "Tailwind Config", "FAIL",
                "tailwind.config.js not found",
                "Create Tailwind configuration file",
                ["npx tailwindcss init"]
            ))
        
        # Check PostCSS configuration
        postcss_config_path = self.frontend_path / "postcss.config.js"
        if postcss_config_path.exists():
            with open(postcss_config_path, 'r') as f:
                postcss_content = f.read()
            
            if "tailwindcss" in postcss_content and "autoprefixer" in postcss_content:
                results.append(DiagnosticResult(
                    "PostCSS Configuration", "PASS",
                    "PostCSS is properly configured with Tailwind",
                    None
                ))
            else:
                results.append(DiagnosticResult(
                    "PostCSS Configuration", "WARNING",
                    "PostCSS may not be properly configured for Tailwind",
                    "Update postcss.config.js with Tailwind plugin",
                    ["Add tailwindcss and autoprefixer to PostCSS plugins"]
                ))
        else:
            results.append(DiagnosticResult(
                "PostCSS Config", "FAIL",
                "postcss.config.js not found",
                "Create PostCSS configuration",
                ["Create postcss.config.js with Tailwind and autoprefixer plugins"]
            ))
        
        # Check for CSS import
        main_css_files = ["src/index.css", "src/main.css", "src/App.css", "styles/tailwind.css"]
        css_found = False
        for css_file in main_css_files:
            css_path = self.frontend_path / css_file
            if css_path.exists():
                with open(css_path, 'r') as f:
                    css_content = f.read()
                if "@tailwind" in css_content:
                    css_found = True
                    results.append(DiagnosticResult(
                        "Tailwind CSS Import", "PASS",
                        f"Tailwind directives found in {css_file}",
                        None
                    ))
                    break
        
        if not css_found:
            results.append(DiagnosticResult(
                "Tailwind CSS Import", "FAIL",
                "Tailwind directives not found in CSS files",
                "Add Tailwind directives to your main CSS file",
                ["Add @tailwind base; @tailwind components; @tailwind utilities; to your CSS"]
            ))
        
        return results
    
    def _check_api_communication(self) -> List[DiagnosticResult]:
        """Check API communication between frontend and backend"""
        results = []
        
        print("\n🔌 Step 4: API Communication")
        print("-" * 40)
        
        # Check for API service files
        api_service_files = ["services/api.js", "utils/api.js", "src/api.js"]
        api_service_found = False
        
        for api_file in api_service_files:
            api_path = self.frontend_path / api_file
            if api_path.exists():
                api_service_found = True
                with open(api_path, 'r') as f:
                    api_content = f.read()
                
                # Check for proper base URL configuration
                if "localhost" in api_content or "baseURL" in api_content:
                    results.append(DiagnosticResult(
                        "API Service Configuration", "PASS",
                        f"API service found in {api_file}",
                        None
                    ))
                else:
                    results.append(DiagnosticResult(
                        "API Service Configuration", "WARNING",
                        "API service exists but may not have proper base URL",
                        "Configure base URL in API service",
                        [f"Set baseURL: 'http://localhost:{self.backend_port}' in axios configuration"]
                    ))
                break
        
        if not api_service_found:
            results.append(DiagnosticResult(
                "API Service", "WARNING",
                "No dedicated API service file found",
                "Create API service for centralized backend communication",
                ["Create services/api.js with axios configuration"]
            ))
        
        # Check environment variables
        env_files = [".env", ".env.local", ".env.development"]
        env_found = False
        
        for env_file in env_files:
            env_path = self.frontend_path / env_file
            if env_path.exists():
                env_found = True
                with open(env_path, 'r') as f:
                    env_content = f.read()
                
                if "VITE_API_URL" in env_content or "VITE_BACKEND_URL" in env_content:
                    results.append(DiagnosticResult(
                        "Environment Variables", "PASS",
                        f"Environment variables configured in {env_file}",
                        None
                    ))
                else:
                    results.append(DiagnosticResult(
                        "Environment Variables", "WARNING",
                        "Environment file exists but no API URL configured",
                        "Add API URL to environment variables",
                        [f"Add VITE_API_URL=http://localhost:{self.backend_port} to {env_file}"]
                    ))
                break
        
        if not env_found:
            results.append(DiagnosticResult(
                "Environment Variables", "WARNING",
                "No environment file found",
                "Create environment file for configuration",
                [f"Create .env file with VITE_API_URL=http://localhost:{self.backend_port}"]
            ))
        
        # Test actual API connectivity
        if self._is_port_accessible(self.backend_port):
            try:
                response = requests.get(f"{self.backend_url}/health", timeout=5)
                if response.status_code == 200:
                    results.append(DiagnosticResult(
                        "API Health Check", "PASS",
                        "Backend API is responding to health checks",
                        None
                    ))
                else:
                    results.append(DiagnosticResult(
                        "API Health Check", "WARNING",
                        f"Backend responded with status {response.status_code}",
                        "Check backend health endpoint",
                        ["Verify /health endpoint exists in backend"]
                    ))
            except requests.exceptions.RequestException as e:
                results.append(DiagnosticResult(
                    "API Health Check", "FAIL",
                    f"Cannot reach backend API: {str(e)}",
                    "Verify backend is running and accessible",
                    ["Check backend server logs", "Verify backend port configuration"]
                ))
        
        return results
    
    def _check_cors_configuration(self) -> List[DiagnosticResult]:
        """Check CORS configuration for local development"""
        results = []
        
        print("\n🔐 Step 5: CORS Configuration")
        print("-" * 40)
        
        # Check backend CORS configuration
        backend_main_files = ["app/main.py", "main.py", "app.py"]
        cors_configured = False
        
        for main_file in backend_main_files:
            main_path = self.backend_path / main_file
            if main_path.exists():
                with open(main_path, 'r') as f:
                    main_content = f.read()
                
                # Check for FastAPI CORS
                if "CORSMiddleware" in main_content:
                    cors_configured = True
                    if "localhost:5173" in main_content or "allow_origins=['*']" in main_content:
                        results.append(DiagnosticResult(
                            "CORS Configuration", "PASS",
                            "CORS is properly configured for local development",
                            None
                        ))
                    else:
                        results.append(DiagnosticResult(
                            "CORS Configuration", "WARNING",
                            "CORS middleware found but may not allow frontend origin",
                            "Update CORS allowed origins",
                            [f"Add 'http://localhost:{self.frontend_port}' to allowed origins"]
                        ))
                # Check for Flask CORS
                elif "flask_cors" in main_content or "CORS" in main_content:
                    cors_configured = True
                    results.append(DiagnosticResult(
                        "CORS Configuration", "PASS",
                        "Flask CORS is configured",
                        None
                    ))
                break
        
        if not cors_configured:
            results.append(DiagnosticResult(
                "CORS Configuration", "FAIL",
                "No CORS configuration found in backend",
                "Add CORS middleware to backend",
                [
                    "For FastAPI: from fastapi.middleware.cors import CORSMiddleware",
                    f"app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:{self.frontend_port}'])"
                ]
            ))
        
        # Test CORS with actual request
        if self._is_port_accessible(self.backend_port):
            try:
                # Simulate preflight request
                headers = {
                    'Origin': f'http://localhost:{self.frontend_port}',
                    'Access-Control-Request-Method': 'GET',
                    'Access-Control-Request-Headers': 'Content-Type'
                }
                response = requests.options(f"{self.backend_url}/health", headers=headers, timeout=5)
                
                if 'Access-Control-Allow-Origin' in response.headers:
                    results.append(DiagnosticResult(
                        "CORS Preflight Test", "PASS",
                        "CORS preflight requests are handled correctly",
                        None
                    ))
                else:
                    results.append(DiagnosticResult(
                        "CORS Preflight Test", "FAIL",
                        "CORS preflight requests are not handled",
                        "Verify CORS configuration handles preflight requests",
                        ["Check CORS middleware configuration for OPTIONS method"]
                    ))
            except requests.exceptions.RequestException:
                results.append(DiagnosticResult(
                    "CORS Preflight Test", "WARNING",
                    "Could not test CORS preflight (backend may not be running)",
                    "Start backend server to test CORS",
                    None
                ))
        
        return results
    
    def _is_port_accessible(self, port: int) -> bool:
        """Check if a port is accessible"""
        try:
            response = requests.get(f"http://localhost:{port}", timeout=2)
            return True
        except requests.exceptions.RequestException:
            return False
    
    def _find_alternative_ports(self, ports: List[int]) -> List[int]:
        """Find available alternative ports"""
        available = []
        for port in ports:
            if not self._is_port_accessible(port):
                available.append(port)
        return available
    
    def print_results(self, results: List[DiagnosticResult]):
        """Print formatted diagnostic results"""
        print("\n" + "=" * 60)
        print("📋 DIAGNOSTIC SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in results if r.status == "PASS")
        failed = sum(1 for r in results if r.status == "FAIL")
        warnings = sum(1 for r in results if r.status == "WARNING")
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⚠️  Warnings: {warnings}")
        print()
        
        for result in results:
            status_icon = {"PASS": "✅", "FAIL": "❌", "WARNING": "⚠️"}[result.status]
            print(f"{status_icon} {result.test_name}: {result.message}")
            
            if result.fix_suggestion:
                print(f"   💡 Fix: {result.fix_suggestion}")
            
            if result.commands:
                print("   🔧 Commands:")
                for cmd in result.commands:
                    print(f"      {cmd}")
            print()
    
    def generate_fix_script(self, results: List[DiagnosticResult]) -> str:
        """Generate a bash script to fix common issues"""
        script_lines = ["#!/bin/bash", "", "# AgentHack 2025 Networking Fix Script", ""]
        
        for result in results:
            if result.status == "FAIL" and result.commands:
                script_lines.append(f"# Fix: {result.test_name}")
                script_lines.extend(result.commands)
                script_lines.append("")
        
        return "\n".join(script_lines)


def main():
    """Main CLI interface for the networking troubleshooter"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AgentHack 2025 Networking Troubleshooter")
    parser.add_argument("--frontend-port", type=int, default=5173, help="Frontend port (default: 5173)")
    parser.add_argument("--backend-port", type=int, default=8000, help="Backend port (default: 8000)")
    parser.add_argument("--frontend-path", default="/workspace/frontend", help="Frontend directory path")
    parser.add_argument("--backend-path", default="/workspace/backend", help="Backend directory path")
    parser.add_argument("--generate-fix-script", action="store_true", help="Generate fix script")
    
    args = parser.parse_args()
    
    troubleshooter = NetworkingTroubleshooter(
        frontend_port=args.frontend_port,
        backend_port=args.backend_port,
        frontend_path=args.frontend_path,
        backend_path=args.backend_path
    )
    
    results = troubleshooter.run_full_diagnosis()
    troubleshooter.print_results(results)
    
    if args.generate_fix_script:
        script_content = troubleshooter.generate_fix_script(results)
        with open("/workspace/fix_networking.sh", "w") as f:
            f.write(script_content)
        print("🔧 Fix script generated: fix_networking.sh")


if __name__ == "__main__":
    main()