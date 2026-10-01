import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  build: {
    // Output directly to the root dist folder
    outDir: '../dist',
    emptyOutDir: true
  },
  server: {
    proxy: {
      // Proxy local API requests to Flask during development
      '/api': 'http://127.0.0.1:5000'
    }
  }
})
