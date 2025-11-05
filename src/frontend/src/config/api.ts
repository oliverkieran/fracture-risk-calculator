/**
 * API Configuration
 * Centralizes API base URL configuration
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const apiConfig = {
  baseURL: API_BASE_URL,
  endpoints: {
    getRisk: '/api/getRisk/',
    getShapPlot: '/api/getShapPlot/',
  },
} as const;

/**
 * Get the full URL for an API endpoint
 */
export const getApiUrl = (endpoint: keyof typeof apiConfig.endpoints): string => {
  return `${apiConfig.baseURL}${apiConfig.endpoints[endpoint]}`;
};
