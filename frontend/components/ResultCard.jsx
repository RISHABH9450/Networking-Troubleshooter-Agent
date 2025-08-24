// ResultCard.jsx
import React from "react";

/**
 * Expect props:
 *  - title: string (DNS, HTTP, SSL, Ping, GeoIP)
 *  - ok: boolean
 *  - children: display raw JSON or text
 */
export default function ResultCard({ title, ok, children }) {
  const base = ok ? "bg-green-50" : "bg-red-50";
  return (
    <div className={`p-4 rounded-2xl shadow ${base}`}>
      <div className="flex items-center justify-between mb-2">
        <div className="font-semibold">{title}</div>
        <div className="text-sm">{ok ? "✅ OK" : "❌ Issue"}</div>
      </div>
      <pre className="text-sm whitespace-pre-wrap">{children}</pre>
    </div>
  );
}
