// api.js
import axios from "axios";

export const api = axios.create({
  // This environment variable will be set by Render at deployment.
  // The fallback is for local development.
  baseURL: import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000",
  timeout: 15000,
});

/**
 * Sends a GET request to the backend's /diagnose endpoint.
 *
 * @param {string} url - The URL to diagnose.
 * @param {string} mode - The explanation mode ('beginner' or 'expert').
 * @returns {Promise<object>} The 'data' payload from the backend's response.
 */
export const diagnose = async (url, mode = "beginner") => {
  try {
    // The backend expects query parameters, so we use axios.get
    // and pass them in the 'params' object.
    const res = await api.get("/diagnose", { params: { url, mode } });

    // If your backend wraps the payload (e.g., {success: True, data: ...}), normalize here.
    if (res.data && res.data.data) return res.data.data;
    return res.data;
  } catch (error) {
    console.error("Error during diagnosis:", error);
    throw error;
  }
};

/**
 * Sends a POST request to download a report from the backend.
 * The backend is expected to return a file blob.
 *
 * @param {string} url - The URL used for the diagnosis.
 * @param {string} mode - The explanation mode.
 */
export const downloadReport = async (url, mode = "beginner") => {
  try {
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
  } catch (error) {
    console.error("Failed to download report:", error);
    // You should use a better way to display this to the user, like a modal.
    console.log("Failed to download report. Please try again.");
  }
};