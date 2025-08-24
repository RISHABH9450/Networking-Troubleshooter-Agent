// api.js
import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000",
  timeout: 15000,
});

export const diagnose = async (url, mode = "beginner") => {
  // backend expects query params for GET or JSON for POST depending on your API
  // This code uses POST /diagnose with JSON body (matches earlier FastAPI examples)
  const payload = { url, mode };
  const res = await api.post("/diagnose", payload);
  // If your backend wraps the payload (e.g., {success: True, data: ...}), normalize here
  if (res.data && res.data.data) return res.data.data;
  return res.data;
};

export const downloadReport = async (url, mode = "beginner") => {
  // POST /report returns a Markdown file blob
  const payload = { url, mode };
  const res = await api.post("/report", payload, { responseType: "blob" });
  const blob = new Blob([res.data], { type: "text/markdown" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "network-report.md";
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(a.href);
};
