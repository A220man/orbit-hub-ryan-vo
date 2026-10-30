export interface HealthResponse {
  status: string;
  version: string;
  service: string;
}

export interface ModelBase {
  name: string;
  description?: string;
  framework: string;
  version: string;
  metadata_json?: string;
}

export interface ModelCreate extends ModelBase {}

export interface ModelUpdate {
  name?: string;
  description?: string;
  framework?: string;
  version?: string;
  metadata_json?: string;
}

export interface ModelResponse extends ModelBase {
  id: string;
  created_at: string;
  updated_at: string;
}

export interface ModelListResponse {
  items: ModelResponse[];
  total: number;
  page: number;
  page_size: number;
}