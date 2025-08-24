import { useState } from "react";
import { diagnose, downloadReport } from "../services/api";
import ResultCard from "../components/ResultCard.jsx";

export default function App() {
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
      <h1 className="text-2xl font-bold">Networking Troubleshooter</h1>

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
