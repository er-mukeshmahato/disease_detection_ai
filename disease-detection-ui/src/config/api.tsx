export const API_BASE = import.meta.env.VITE_API_BASE;

export const API_ROUTES = {
  UPLOAD: `${API_BASE}/predict/upload/`,
  EXPLAIN: `${API_BASE}/predict/explain/`,
  DOWNLOAD_REPORT: `${API_BASE}/predict/download-report/`,
};
