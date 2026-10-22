import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, waitFor } from '@testing-library/react';
import { HealthStatus } from './HealthStatus';
import { api } from '../api/client';

vi.mock('../api/client', () => ({
  api: {
    health: {
      get: vi.fn(),
    },
  },
}));

describe('HealthStatus', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('shows loading state initially', () => {
    api.health.get.mockImplementation(() => new Promise(() => {}));

    const { container } = render(<HealthStatus />);

    expect(container.querySelector('.loading')).toBeInTheDocument();
    expect(container.querySelector('.loading')?.textContent).toContain('Checking backend health');
  });

  it('displays healthy status when API succeeds', async () => {
    api.health.get.mockResolvedValue({
      status: 'healthy',
      version: '1.0.0',
      service: 'Orbit Hub',
    });

    const { container } = render(<HealthStatus />);

    await waitFor(() => {
      expect(container.querySelector('h2')).toBeInTheDocument();
      expect(container.querySelector('h2')?.textContent).toBe('Backend Health');
    });

    expect(container.querySelector('.status-healthy')).toBeInTheDocument();
    expect(container.querySelector('.status-healthy')?.textContent).toBe('healthy');
    expect(container.textContent).toContain('Orbit Hub');
    expect(container.textContent).toContain('1.0.0');
  });

  it('displays error when API fails', async () => {
    api.health.get.mockRejectedValue(new Error('Network error'));

    const { container } = render(<HealthStatus />);

    await waitFor(() => {
      expect(container.querySelector('.error')).toBeInTheDocument();
      expect(container.querySelector('.error')?.textContent).toContain('Network error');
    });
  });
});