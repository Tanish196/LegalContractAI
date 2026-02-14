import React from 'react';
import { createRoot } from 'react-dom/client';

console.log('[MINIMAL TEST] Starting minimal React test...');

try {
    const root = document.getElementById('root');
    if (!root) {
        throw new Error('Root element not found');
    }

    console.log('[MINIMAL TEST] Root element found, rendering simple component...');

    createRoot(root).render(
        <div style={{ padding: '40px', fontFamily: 'Arial' }}>
            <h1 style={{ color: 'green' }}>✓ React is Working!</h1>
            <p>If you see this, React is rendering correctly.</p>
            <p>The white screen issue is likely caused by a component error.</p>

            <details style={{ marginTop: '20px' }}>
                <summary style={{ cursor: 'pointer', fontWeight: 'bold' }}>Click to see diagnostic info</summary>
                <pre style={{ background: '#f5f5f5', padding: '15px', marginTop: '10px' }}>
                    {JSON.stringify({
                        'React': 'Working',
                        'Root Element': 'Found',
                        'Environment': {
                            VITE_SUPABASE_URL: import.meta.env.VITE_SUPABASE_URL || 'MISSING',
                            VITE_GEMINI_API_KEY: import.meta.env.VITE_GEMINI_API_KEY ? 'SET' : 'MISSING',
                        }
                    }, null, 2)}
                </pre>
            </details>

            <button
                onClick={() => window.location.href = '/'}
                style={{
                    marginTop: '20px',
                    padding: '10px 20px',
                    background: '#3b82f6',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer'
                }}
            >
                Try Loading Full App
            </button>
        </div>
    );

    console.log('[MINIMAL TEST] Minimal app rendered successfully');
} catch (error) {
    console.error('[MINIMAL TEST] Error during render:', error);
    const root = document.getElementById('root');
    if (root) {
        root.innerHTML = `
      <div style="padding: 20px; font-family: monospace; color: red;">
        <h1>Minimal Test Failed</h1>
        <pre style="background: #fee; padding: 15px; border-radius: 4px;">
${error instanceof Error ? error.stack : String(error)}
        </pre>
      </div>
    `;
    }
}
