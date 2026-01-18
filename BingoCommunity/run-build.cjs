#!/usr/bin/env node

/**
 * run-build.js
 * Cloudflare Pages–safe build script
 */

const { execSync } = require("child_process");
const process = require("process");

const REQUIRED_ENVS = [
  "VITE_API_URL",
  "VITE_SUPABASE_URL",
  "VITE_SUPABASE_ANON_KEY"
];

function checkEnv() {
  const missing = REQUIRED_ENVS.filter(
    key => !process.env[key]
  );

  if (missing.length) {
    console.error("❌ Missing required environment variables:");
    missing.forEach(k => console.error(`   - ${k}`));
    process.exit(1);
  }
}

function run(cmd) {
  console.log(`\n▶ ${cmd}`);
  execSync(cmd, { stdio: "inherit" });
}

try {
  console.log("🔍 Validating environment variables...");
  checkEnv();

  console.log("📦 Installing dependencies...");
  run("npm install");

  console.log("🏗️  Building production bundle...");
  run("npm run build");

  console.log("\n✅ Build completed successfully.");
} catch (err) {
  console.error("\n❌ Build failed.");
  process.exit(1);
}
