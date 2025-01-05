import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  define: {
    'global': 'globalThis',
    'process.env': {}
  },
  build: {
    commonjsOptions: {
      transformMixedEsModules: true
    }
  },
  resolve: {
    alias: {
      events: 'events',
      crypto: 'crypto-browserify',
      stream: 'stream-browserify',
      http: 'stream-http',
      https: 'https-browserify',
      os: 'os-browserify/browser'
    }
  }
});