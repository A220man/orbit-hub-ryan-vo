
const API_BASE = '/api/v1';

async function fetchJson<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

import type { HealthResponse, ModelResponse, ModelListResponse, ModelCreate, ModelUpdate } from '../types/api';

export const api = {
  health: {
    get: () => fetchJson<HealthResponse>('/health'),
  },
  models: {
    list: (params?: { page?: number; page_size?: number; name?: string; framework?: string }) => {
      const searchParams = new URLSearchParams();
      if (params?.page) searchParams.set('page', params.page.toString());
      if (params?.page_size) searchParams.set('page_size', params.page_size.toString());
      if (params?.name) searchParams.set('name', params.name);
      if (params?.framework) searchParams.set('framework', params.framework);
      const query = searchParams.toString();
      return fetchJson<ModelListResponse>(`/models${query ? `?${query}` : ''}`);
    },
    get: (id: string) => fetchJson<ModelResponse>(`/models/${id}`),
    create: (data: ModelCreate) =>
      fetchJson<ModelResponse>('/models', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    update: (id: string, data: ModelUpdate) =>
      fetchJson<ModelResponse>(`/models/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
      }),
    delete: (id: string) =>
      fetch(`/api/v1/models/${id}`, { method: 'DELETE' }).then((res) => {
        if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
      }),
  },
};
