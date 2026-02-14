console.log('[MAIN.TSX] Starting application initialization...');

// Prevent theme flash
const initializeTheme = () => {
  try {
    console.log('[MAIN.TSX] Initializing theme...');
    const theme = localStorage.getItem('vite-ui-theme') || 'system';
    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      document.documentElement.classList.add(systemTheme);
      document.documentElement.setAttribute('data-theme', systemTheme);
    } else {
      document.documentElement.classList.add(theme);
      document.documentElement.setAttribute('data-theme', theme);
    }
    console.log('[MAIN.TSX] Theme initialized:', theme);
  } catch (error) {
    console.error('[MAIN.TSX] Theme initialization failed:', error);
  }
};

initializeTheme();

console.log('[MAIN.TSX] Importing React modules...');

import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import './index.css'

console.log('[MAIN.TSX] Modules imported successfully');
console.log('[MAIN.TSX] Environment variables:', {
  VITE_SUPABASE_URL: import.meta.env.VITE_SUPABASE_URL,
  VITE_SUPABASE_ANON_KEY: import.meta.env.VITE_SUPABASE_ANON_KEY ? '***' : 'MISSING',
  VITE_API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000 (default)'
});

try {
  const root = document.getElementById('root')
  if (!root) {
    console.error('[MAIN.TSX] Root element not found!');
    throw new Error('Root element not found')
  }

  console.log('[MAIN.TSX] Root element found, creating React root...');

  createRoot(root).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );

  console.log('[MAIN.TSX] React app rendered successfully');
} catch (error) {
  console.error('[MAIN.TSX] FATAL ERROR during React initialization:', error);
  // Display error on screen
  const root = document.getElementById('root');
  if (root) {
    root.innerHTML = `
      <div style="padding: 20px; font-family: monospace;">
        <h1 style="color: red;">Application Failed to Initialize</h1>
        <pre style="background: #f0f0f0; padding: 10px; border-radius: 4px; overflow: auto;">
${error instanceof Error ? error.stack : String(error)}
        </pre>
        <p>Check the browser console for more details.</p>
      </div>
    `;
  }
}
