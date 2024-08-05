import { INTERNAL_URL } from "./env";

function buildUrl(path: string): string {
  if (!path.startsWith("/")) {
    path = `/${path}`;
  }
  return new URL(`/api${path}`, INTERNAL_URL).toString();
}

export async function fetchServer(
  url: string,
  options?: RequestInit,
): Promise<{ loading: boolean; data: any | null; error: Error | null }> {
  const init: RequestInit = {
    ...options,
    credentials: "include",
    headers: {
      ...options?.headers,
      "Content-Type": "application/json",
    },
  };

  const response = await fetch(buildUrl(url), init);
  const data = await response.json();
  if (response.ok) {
    return { loading: false, data, error: null };
  } else {
    const errorMessage = data.detail || data.message || data.status;
    return { loading: false, data: null, error: errorMessage };
  }
}

export async function fetchSS(
  url: string,
  options?: RequestInit,
): Promise<any> {
  const init: RequestInit = {
    ...options,
    credentials: "include",
    headers: {
      ...options?.headers,
      "Content-Type": "application/json",
    },
  };

  const response = await fetch(buildUrl(url), init);
  if (response.ok) {
    return response.json();
  } else {
    throw new Error(response.statusText);
  }
}
