// adapter for node
import adapter from "@sveltejs/adapter-node";
import { vitePreprocess } from "@sveltejs/kit/vite";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    adapter: adapter(),
  },
  // Enable use of PostCSS in <style> blocks
  preprocess: vitePreprocess(),
};

export default config;
