// All requests go through the Go gateway service, which forwards to Django
// and applies shared concerns (CORS, timeouts, request logging).
const GATEWAY_BASE_URL = import.meta.env.VITE_GATEWAY_URL || "http://localhost:8080";

const TOKEN_KEY = "mediflow_access_token";
const REFRESH_KEY = "mediflow_refresh_token";

export function getAccessToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_KEY);
}

export function setTokens({ access, refresh }) {
  if (access) localStorage.setItem(TOKEN_KEY, access);
  if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
}

export function clearTokens() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_KEY);
}

async function request(path, { method = "GET", body, auth = false } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (auth) {
    const token = getAccessToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${GATEWAY_BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  let data = null;
  try {
    data = await res.json();
  } catch {
    // some endpoints (e.g. logout) may return no body
  }

  if (!res.ok) {
    const message =
      (data && (data.detail || Object.values(data).flat().join(" "))) ||
      `Request failed with status ${res.status}`;
    throw new Error(message);
  }

  return data;
}

export const authApi = {
  loginStudent: (unique_id, password) =>
    request("/api/auth/login", { method: "POST", body: { unique_id, password } }),

  registerStudent: (payload) =>
    request("/api/auth/register/student", { method: "POST", body: payload }),

  registerStaff: (payload) =>
    request("/api/auth/register/staff", { method: "POST", body: payload, auth: true }),

  refreshToken: (refresh) =>
    request("/api/auth/token/refresh", { method: "POST", body: { refresh } }),

  logout: (refresh) =>
    request("/api/auth/logout", { method: "POST", body: { refresh }, auth: true }),

  changePassword: (payload) =>
    request("/api/auth/change-password", { method: "POST", body: payload, auth: true }),
};
