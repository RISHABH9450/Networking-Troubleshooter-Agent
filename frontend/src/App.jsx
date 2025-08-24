import { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from "react-router-dom";
import { diagnose, downloadReport } from "../services/api";
import ResultCard from "../components/ResultCard.jsx";
import TroubleshooterDashboard from "./TroubleshooterDashboard.jsx";

// Original Networking Troubleshooter Component
function OriginalTroubleshooter() {
  const [url, setUrl] = useState("https://example.com");
  const [mode, setMode] = useState("beginner");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const onRun = async () => {
    setLoading(true);
    try {
      const res = await diagnose(url, mode);
      setData(res);
    } finally {
      setLoading(false);
    }
  };

  const onDownload = async () => {
    if (!data) return;
    await downloadReport(data, url);
  };

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">Network Diagnostics</h1>
      <p className="text-gray-600">Test DNS, SSL, HTTP, Ping, and GeoIP for any domain or IP</p>

      {/* Input controls */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 items-end">
        <div className="sm:col-span-3">
          <label className="block text-sm mb-1">Website URL</label>
          <input
            className="w-full border rounded-xl p-3"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
        </div>
        <div>
          <label className="block text-sm mb-1">Mode</label>
          <select
            className="w-full border rounded-xl p-3"
            value={mode}
            onChange={(e) => setMode(e.target.value)}
          >
            <option value="beginner">Beginner</option>
            <option value="expert">Expert</option>
          </select>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex gap-3">
        <button
          onClick={onRun}
          className="bg-blue-600 text-white rounded-xl px-4 py-2 hover:bg-blue-700"
          disabled={loading}
        >
          {loading ? "Running..." : "Run Diagnosis"}
        </button>
        {data && (
          <button
            onClick={onDownload}
            className="bg-green-600 text-white rounded-xl px-4 py-2 hover:bg-green-700"
          >
            Download Report
          </button>
        )}
      </div>

      {/* Results */}
      {data && (
        <div className="space-y-4">
          {Object.entries(data).map(([tool, result], idx) => (
            <ResultCard key={idx} tool={tool} result={result} />
          ))}
        </div>
      )}
    </div>
  );
}

// Navigation Component
function Navigation() {
  const location = useLocation();
  
  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-4">
            <h1 className="text-xl font-bold text-gray-900">Networking Troubleshooter</h1>
          </div>
          <div className="flex space-x-4">
            <Link
              to="/"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                location.pathname === '/' 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              🌐 Network Diagnostics
            </Link>
            <Link
              to="/agenthack"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                location.pathname === '/agenthack' 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              🔧 AgentHack 2025
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

// Main App Component with Routing
export default function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <Routes>
          <Route path="/" element={<OriginalTroubleshooter />} />
          <Route path="/agenthack" element={<TroubleshooterDashboard />} />
          <Route path="/login" element={
            <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
              <h2 className="text-2xl font-bold mb-4">Login Page</h2>
              <p className="text-gray-600">This is a demo login page for testing routing.</p>
            </div>
          } />
          <Route path="/dashboard" element={
            <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
              <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
              <p className="text-gray-600">This is a demo dashboard page for testing routing.</p>
            </div>
          } />
          <Route path="/tasks" element={
            <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
              <h2 className="text-2xl font-bold mb-4">Tasks</h2>
              <p className="text-gray-600">This is a demo tasks page for testing routing.</p>
            </div>
          } />
        </Routes>
      </div>
    </Router>
  );
}
