import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],

  server: {
    port: 5173,
    strictPort: true
  },

  build: {
    outDir: "dist",
    sourcemap: false,
    target: "es2020",
    emptyOutDir: true
  },

  define: {
    __APP_ENV__: JSON.stringify(process.env.NODE_ENV)
  }
});