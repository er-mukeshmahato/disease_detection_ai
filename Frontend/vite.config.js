import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Vite config
export default {
  server: {
    host: '0.0.0.0',  // Ensures app listens on all network interfaces
    port: 3000,        // Correct port for Vite
  },
};
