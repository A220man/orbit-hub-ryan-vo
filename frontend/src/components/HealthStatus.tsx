import { useState, useEffect } from 'react';
import { api } from '../api/client';
import type { HealthResponse } from '../types/api';

export function HealthStatus() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchHealth() {
      try {
        setLoading(true);
        const data = await api.health.get();
        setHealth(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
        setHealth(null);
      } finally {
        setLoading(false);
      }
    }

    fetchHealth();
    const interval = setInterval(fetchHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="loading">Checking backend health...</div>;
  }

  if (error) {
    return <div className="error">Failed to connect: {error}</div>;
  }

  if (!health) {
    return <div className="error">No health data</div>;
  }

  return (
    <div className="card">
      <h2>Backend Health</h2>
      <div style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <div>
          <strong>Status:</strong>{' '}
          <span className={health.status === 'healthy' ? 'status-healthy' : 'status-unhealthy'}>
            {health.status}
          </span>
        </div>
        <div><strong>Service:</strong> {health.service}</div>
        <div><strong>Version:</strong> {health.version}</div>
      </div>
    </div>
  );
}