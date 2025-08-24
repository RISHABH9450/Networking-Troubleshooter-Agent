// ReportCard.jsx
import React from "react";

/**
 * Small card to show health score and quick actions
 * props:
 *  - score: number
 *  - onDownload: fn
 */
export default function ReportCard({ score = 0, onDownload }) {
  const color =
    score >= 80 ? "text-green-600" : score >= 50 ? "text-yellow-600" : "text-red-600";

  return (
    <div className="p-4 rounded-2xl border flex items-center justify-between">
      <div>
        <div className="text-sm text-gray-500">Health Score</div>
        <div className={`text-2xl font-bold ${color}`}>{score}/100</div>
      </div>
      <div>
        <button
          onClick={onDownload}
          className="px-4 py-2 rounded-xl bg-gray-800 text-white hover:bg-gray-900"
        >
          Download Report
        </button>
      </div>
    </div>
  );
}
