// InputForm.jsx
import React from "react";

export default function InputForm({ url, setUrl, mode, setMode, onRun, loading }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 items-end">
      <div className="sm:col-span-3">
        <label className="block text-sm mb-1">Website URL</label>
        <input
          className="w-full border rounded-xl p-3"
          value={url}
          placeholder="https://example.com or example.com"
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

      <div className="sm:col-span-4 flex gap-3 mt-2">
        <button
          onClick={onRun}
          disabled={loading}
          className="bg-blue-600 text-white rounded-xl px-4 py-2 hover:bg-blue-700 disabled:opacity-60"
        >
          {loading ? "Running..." : "Run Diagnosis"}
        </button>
      </div>
    </div>
  );
}
