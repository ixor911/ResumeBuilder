import axios, {
  AxiosError,
  AxiosHeaders,
  type InternalAxiosRequestConfig,
} from "axios";

import type { AuthTokens } from "./models";

type RefreshTokenResponse = {
  access: string;
  refresh?: string;
};

type RetryableRequestConfig = InternalAxiosRequestConfig & {
  _retry?: boolean;
};

const AUTH_STORAGE_KEY = "resumeBuilder.authTokens";

function normalizeBaseUrl(url: string) {
  return url.replace(/\/+$/, "");
}

function canUseLocalStorage() {
  return typeof window !== "undefined" && Boolean(window.localStorage);
}

function readStoredTokens(): AuthTokens | null {
  if (!canUseLocalStorage()) {
    return null;
  }

  try {
    const rawTokens = window.localStorage.getItem(AUTH_STORAGE_KEY);
    if (!rawTokens) {
      return null;
    }

    const parsed = JSON.parse(rawTokens) as Partial<AuthTokens>;
    if (typeof parsed.access === "string" && typeof parsed.refresh === "string") {
      return {
        access: parsed.access,
        refresh: parsed.refresh,
      };
    }
  } catch {
    window.localStorage.removeItem(AUTH_STORAGE_KEY);
  }

  return null;
}

export const API_BASE_URL = normalizeBaseUrl(
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api",
);

let authTokens = readStoredTokens();
let refreshRequest: Promise<string | null> | null = null;

export const apiConnector = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export function getAuthTokens() {
  return authTokens;
}

export function setAuthTokens(tokens: AuthTokens) {
  authTokens = tokens;

  if (canUseLocalStorage()) {
    window.localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(tokens));
  }
}

export function clearAuthTokens() {
  authTokens = null;

  if (canUseLocalStorage()) {
    window.localStorage.removeItem(AUTH_STORAGE_KEY);
  }
}

export function hasAuthTokens() {
  return Boolean(authTokens?.access && authTokens?.refresh);
}

export function buildApiUrl(path: string) {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return `${API_BASE_URL}${normalizedPath}`;
}

async function refreshAccessToken() {
  const tokens = getAuthTokens();
  if (!tokens?.refresh) {
    return null;
  }

  const response = await axios.post<RefreshTokenResponse>(
    buildApiUrl("/auth/refresh/"),
    { refresh: tokens.refresh },
  );

  const nextTokens = {
    access: response.data.access,
    refresh: response.data.refresh ?? tokens.refresh,
  };
  setAuthTokens(nextTokens);

  return nextTokens.access;
}

apiConnector.interceptors.request.use((config) => {
  const tokens = getAuthTokens();
  if (tokens?.access) {
    const headers = AxiosHeaders.from(config.headers);
    headers.set("Authorization", `Bearer ${tokens.access}`);
    config.headers = headers;
  }

  return config;
});

apiConnector.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as RetryableRequestConfig | undefined;
    const isRefreshRequest = originalRequest?.url?.includes("/auth/refresh/");

    if (
      error.response?.status !== 401 ||
      !originalRequest ||
      originalRequest._retry ||
      isRefreshRequest
    ) {
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    try {
      refreshRequest ??= refreshAccessToken().finally(() => {
        refreshRequest = null;
      });

      const nextAccessToken = await refreshRequest;
      if (!nextAccessToken) {
        clearAuthTokens();
        return Promise.reject(error);
      }

      const headers = AxiosHeaders.from(originalRequest.headers);
      headers.set("Authorization", `Bearer ${nextAccessToken}`);
      originalRequest.headers = headers;

      return apiConnector(originalRequest);
    } catch {
      clearAuthTokens();
      return Promise.reject(error);
    }
  },
);
