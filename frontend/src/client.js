/**
 * API Client Configuration
 * 
 * Centralized axios instance configured to communicate with the backend.
 * Uses the VITE_API_URL environment variable for the base URL.
 * 
 * Environment variables:
 * - VITE_API_URL: Backend API URL (default: http://localhost:8000)
 */

import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

/**
 * Error interceptor for better error handling
 */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default api;