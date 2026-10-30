
import type { ModelResponse } from '../types/api';

interface ModelCardProps {
  model: ModelResponse;
  onEdit?: (model: ModelResponse) => void;
  onDelete?: (id: string) => void;
  isDeleting?: boolean;
}

export function ModelCard({ model, onEdit, onDelete, isDeleting }: ModelCardProps) {
  return (
    <div className="model-card">
      <div className="model-header">
        <h3>{model.name}</h3>
        <span className="model-framework">{model.framework}</span>
      </div>
      <div className="model-meta">
        <span className="model-version">v{model.version}</span>
        <span className="model-id">{model.id.slice(0, 8)}...</span>
      </div>
      {model.description && (
        <p className="model-description">{model.description}</p>
      )}
      <div className="model-timestamps">
        <span>Created: {new Date(model.created_at).toLocaleDateString()}</span>
        <span>Updated: {new Date(model.updated_at).toLocaleDateString()}</span>
      </div>
      <div className="model-actions">
        {onEdit && (
          <button className="btn btn-secondary" onClick={() => onEdit(model)}>
            Edit
          </button>
        )}
        {onDelete && (
          <button
            className="btn btn-danger"
            onClick={() => onDelete(model.id)}
            disabled={isDeleting}
          >
            {isDeleting ? 'Deleting...' : 'Delete'}
          </button>
        )}
      </div>
    </div>
  );
}
