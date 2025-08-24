import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TroubleshooterDashboard = () => {
  const [diagnostics, setDiagnostics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [quickStatus, setQuickStatus] = useState(null);
  const [config, setConfig] = useState({
    frontend_port: 5173,
    backend_port: 8000,
    frontend_path: '/workspace/frontend',
    backend_path: '/workspace/backend'
  });

  const API_BASE = 'http://localhost:8000';

  // Quick connectivity check on component mount
  useEffect(() => {
    checkQuickStatus();
  }, []);

  const checkQuickStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE}/troubleshooter/quick-check`);
      setQuickStatus(response.data);
    } catch (error) {
      console.error('Quick check failed:', error);
      setQuickStatus({
        frontend: { status: 'unknown', url: 'http://localhost:5173' },
        backend: { status: 'unknown', url: 'http://localhost:8000' },
        overall_status: 'connection_failed'
      });
    }
  };

  const runDiagnosis = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE}/troubleshooter/diagnose`, config);
      setDiagnostics(response.data);
    } catch (error) {
      console.error('Diagnosis failed:', error);
      setDiagnostics({
        summary: { failed: 1, passed: 0, warnings: 0, total: 1 },
        results: [{
          test_name: 'Connection Test',
          status: 'FAIL',
          message: 'Could not connect to backend API',
          fix_suggestion: 'Ensure backend server is running on port 8000'
        }]
      });
    }
    setLoading(false);
  };

  const downloadFixScript = () => {
    if (diagnostics?.fix_script) {
      const blob = new Blob([diagnostics.fix_script], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'fix_networking.sh';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'PASS': return '✅';
      case 'FAIL': return '❌';
      case 'WARNING': return '⚠️';
      case 'online': return '🟢';
      case 'offline': return '🔴';
      default: return '⚪';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'PASS':
      case 'online':
      case 'healthy': return 'text-green-600';
      case 'FAIL':
      case 'offline': return 'text-red-600';
      case 'WARNING': return 'text-yellow-600';
      default: return 'text-gray-600';
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            🔧 AgentHack 2025 Networking Troubleshooter
          </h1>
          <p className="text-gray-600">
            Debug frontend-backend connectivity, CORS, routing, and Tailwind CSS issues
          </p>
        </div>

        {/* Quick Status */}
        {quickStatus && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4">🚀 Quick Status Check</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <span className="font-medium">Frontend (React + Vite)</span>
                <div className="flex items-center space-x-2">
                  <span className={getStatusColor(quickStatus.frontend.status)}>
                    {getStatusIcon(quickStatus.frontend.status)} {quickStatus.frontend.status}
                  </span>
                  <code className="text-sm bg-gray-200 px-2 py-1 rounded">
                    {quickStatus.frontend.url}
                  </code>
                </div>
              </div>
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <span className="font-medium">Backend (Python API)</span>
                <div className="flex items-center space-x-2">
                  <span className={getStatusColor(quickStatus.backend.status)}>
                    {getStatusIcon(quickStatus.backend.status)} {quickStatus.backend.status}
                  </span>
                  <code className="text-sm bg-gray-200 px-2 py-1 rounded">
                    {quickStatus.backend.url}
                  </code>
                </div>
              </div>
            </div>
            <div className="text-center">
              <span className={`font-semibold ${getStatusColor(quickStatus.overall_status)}`}>
                Overall Status: {quickStatus.overall_status.replace('_', ' ').toUpperCase()}
              </span>
            </div>
          </div>
        )}

        {/* Configuration */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">⚙️ Configuration</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Frontend Port
              </label>
              <input
                type="number"
                value={config.frontend_port}
                onChange={(e) => setConfig({...config, frontend_port: parseInt(e.target.value)})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Backend Port
              </label>
              <input
                type="number"
                value={config.backend_port}
                onChange={(e) => setConfig({...config, backend_port: parseInt(e.target.value)})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={runDiagnosis}
              disabled={loading}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></div>
                  <span>Running Diagnosis...</span>
                </>
              ) : (
                <>
                  <span>🔍</span>
                  <span>Run Full Diagnosis</span>
                </>
              )}
            </button>
            <button
              onClick={checkQuickStatus}
              className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 flex items-center justify-center space-x-2"
            >
              <span>⚡</span>
              <span>Quick Check</span>
            </button>
          </div>
        </div>

        {/* Results */}
        {diagnostics && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">📋 Diagnostic Results</h2>
            
            {/* Summary */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="text-center p-3 bg-green-50 rounded">
                <div className="text-2xl font-bold text-green-600">{diagnostics.summary.passed}</div>
                <div className="text-sm text-green-700">Passed</div>
              </div>
              <div className="text-center p-3 bg-red-50 rounded">
                <div className="text-2xl font-bold text-red-600">{diagnostics.summary.failed}</div>
                <div className="text-sm text-red-700">Failed</div>
              </div>
              <div className="text-center p-3 bg-yellow-50 rounded">
                <div className="text-2xl font-bold text-yellow-600">{diagnostics.summary.warnings}</div>
                <div className="text-sm text-yellow-700">Warnings</div>
              </div>
              <div className="text-center p-3 bg-blue-50 rounded">
                <div className="text-2xl font-bold text-blue-600">{diagnostics.summary.total}</div>
                <div className="text-sm text-blue-700">Total Tests</div>
              </div>
            </div>

            {/* Detailed Results */}
            <div className="space-y-4">
              {diagnostics.results.map((result, index) => (
                <div key={index} className="border rounded-lg p-4">
                  <div className="flex items-start space-x-3">
                    <span className="text-xl">{getStatusIcon(result.status)}</span>
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900">{result.test_name}</h3>
                      <p className="text-gray-700 mt-1">{result.message}</p>
                      
                      {result.fix_suggestion && (
                        <div className="mt-3 p-3 bg-blue-50 rounded">
                          <p className="text-sm font-medium text-blue-800">💡 Suggested Fix:</p>
                          <p className="text-sm text-blue-700 mt-1">{result.fix_suggestion}</p>
                        </div>
                      )}
                      
                      {result.commands && result.commands.length > 0 && (
                        <div className="mt-3 p-3 bg-gray-50 rounded">
                          <p className="text-sm font-medium text-gray-800">🔧 Commands:</p>
                          <div className="mt-1 space-y-1">
                            {result.commands.map((cmd, cmdIndex) => (
                              <code key={cmdIndex} className="block text-sm text-gray-700 bg-white px-2 py-1 rounded border">
                                {cmd}
                              </code>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Fix Script */}
            {diagnostics.fix_script && (
              <div className="mt-6 pt-6 border-t">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-lg font-semibold">🔧 Automated Fix Script</h3>
                  <button
                    onClick={downloadFixScript}
                    className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 flex items-center space-x-2"
                  >
                    <span>📥</span>
                    <span>Download Script</span>
                  </button>
                </div>
                <pre className="bg-gray-900 text-green-400 p-4 rounded overflow-x-auto text-sm">
                  {diagnostics.fix_script}
                </pre>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default TroubleshooterDashboard;