
import { useState, useEffect } from 'react';
import { api } from '../api/client';
import type { ModelResponse, ModelListResponse, ModelCreate, ModelUpdate } from '../types/api';
import { ModelCard } from './ModelCard';

export function ModelRegistry() {
  const [models, setModels] = useState<ModelResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pagination, setPagination] = useState({ page: 1, page_size: 10, total: 0 });
  const [filters, setFilters] = useState({ name: '', framework: '' });
  const [showForm, setShowForm] = useState(false);
  const [editingModel, setEditingModel] = useState<ModelResponse | null>(null);
  const [formData, setFormData] = useState<ModelCreate>({
    name: '',
    description: '',
    framework: '',
    version: '',
    metadata_json: '',
  });
  const [formError, setFormError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const fetchModels = async () => {
    try {
      setLoading(true);
      const data = await api.models.list({
        page: pagination.page,
        page_size: pagination.page_size,
        name: filters.name || undefined,
        framework: filters.framework || undefined,
      });
      setModels(data.items);
      setPagination((prev) => ({ ...prev, total: data.total }));
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch models');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchModels();
  }, [pagination.page, filters.name, filters.framework]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);
    setSubmitting(true);

    try {
      if (editingModel) {
        await api.models.update(editingModel.id, formData);
      } else {
        await api.models.create(formData);
      }
      setShowForm(false);
      setEditingModel(null);
      setFormData({ name: '', description: '', framework: '', version: '', metadata_json: '' });
      fetchModels();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : 'Failed to save model');
    } finally {
      setSubmitting(false);
    }
  };

  const handleEdit = (model: ModelResponse) => {
    setEditingModel(model);
    setFormData({
      name: model.name,
      description: model.description || '',
      framework: model.framework,
      version: model.version,
      metadata_json: model.metadata_json || '',
    });
    setShowForm(true);
    setFormError(null);
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this model?')) return;
    setDeletingId(id);
    try {
      await api.models.delete(id);
      fetchModels();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete model');
    } finally {
      setDeletingId(null);
    }
  };

  const handleNewModel = () => {
    setEditingModel(null);
    setFormData({ name: '', description: '', framework: '', version: '', metadata_json: '' });
    setShowForm(true);
    setFormError(null);
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingModel(null);
    setFormError(null);
  };

  const handlePageChange = (newPage: number) => {
    setPagination((prev) => ({ ...prev, page: newPage }));
  };

  const totalPages = Math.ceil(pagination.total / pagination.page_size) || 1;

  if (loading && models.length === 0) {
    return <div className="loading">Loading models...</div>;
  }

  if (error && models.length === 0) {
    return <div className="error">Failed to load models: {error}</div>;
  }

  return (
    <div className="model-registry">
      <div className="registry-header">
        <h2>Model Registry</h2>
        <button className="btn btn-primary" onClick={handleNewModel}>
          + New Model
        </button>
      </div>

      {showForm && (
        <div className="model-form-overlay" onClick={handleCancel}>
          <div className="model-form" onClick={(e) => e.stopPropagation()}>
            <h3>{editingModel ? 'Edit Model' : 'Create Model'}</h3>
            {formError && <div className="form-error">{formError}</div>}
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="name">Name *</label>
                <input
                  id="name"
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                  disabled={submitting}
                />
              </div>
              <div className="form-group">
                <label htmlFor="framework">Framework *</label>
                <input
                  id="framework"
                  type="text"
                  value={formData.framework}
                  onChange={(e) => setFormData({ ...formData, framework: e.target.value })}
                  required
                  disabled={submitting}
                />
              </div>
              <div className="form-group">
                <label htmlFor="version">Version *</label>
                <input
                  id="version"
                  type="text"
                  value={formData.version}
                  onChange={(e) => setFormData({ ...formData, version: e.target.value })}
                  required
                  disabled={submitting}
                />
              </div>
              <div className="form-group">
                <label htmlFor="description">Description</label>
                <textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  rows={3}
                  disabled={submitting}
                />
              </div>
              <div className="form-group">
                <label htmlFor="metadata_json">Metadata (JSON)</label>
                <textarea
                  id="metadata_json"
                  value={formData.metadata_json}
                  onChange={(e) => setFormData({ ...formData, metadata_json: e.target.value })}
                  rows={3}
                  disabled={submitting}
                  placeholder='{"key": "value"}'
                />
              </div>
              <div className="form-actions">
                <button type="button" className="btn btn-secondary" onClick={handleCancel} disabled={submitting}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary" disabled={submitting}>
                  {submitting ? 'Saving...' : editingModel ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="filters">
        <input
          type="text"
          placeholder="Filter by name..."
          value={filters.name}
          onChange={(e) => setFilters({ ...filters, name: e.target.value })}
          onKeyDown={(e) => e.key === 'Enter' && setPagination((p) => ({ ...p, page: 1 }))}
        />
        <input
          type="text"
          placeholder="Filter by framework..."
          value={filters.framework}
          onChange={(e) => setFilters({ ...filters, framework: e.target.value })}
          onKeyDown={(e) => e.key === 'Enter' && setPagination((p) => ({ ...p, page: 1 }))}
        />
      </div>

      <div className="models-grid">
        {models.length === 0 ? (
          <div className="empty-state">No models found. Click "New Model" to create one.</div>
        ) : (
          models.map((model) => (
            <ModelCard
              key={model.id}
              model={model}
              onEdit={handleEdit}
              onDelete={handleDelete}
              isDeleting={deletingId === model.id}
            />
          ))
        )}
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button
            className="btn btn-secondary"
            onClick={() => handlePageChange(pagination.page - 1)}
            disabled={pagination.page <= 1}
          >
            Previous
          </button>
          <span>
            Page {pagination.page} of {totalPages} (Total: {pagination.total})
          </span>
          <button
            className="btn btn-secondary"
            onClick={() => handlePageChange(pagination.page + 1)}
            disabled={pagination.page >= totalPages}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
