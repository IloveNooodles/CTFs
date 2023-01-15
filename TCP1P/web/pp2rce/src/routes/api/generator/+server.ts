import { json } from "@sveltejs/kit";

function isObject(obj: any) {
  return typeof obj === "function" || typeof obj === "object";
}
function merge(target: any, source: any) {
  for (const key in source) {
    if (isObject(target[key]) && isObject(source[key])) {
      merge(target[key], source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

function clone(target: any) {
  const DEFAULT_TARGET = {
    "name": "my-app",
    "version": "0.0.1",
    "scripts": {
      "dev": "node app.js",
    },
    "devDependencies": {},
    "type": "module",
    "dependencies": {},
  };
  return merge(DEFAULT_TARGET, target);
}

import type * as kit from "@sveltejs/kit";
export const POST: kit.RequestHandler = async ({ request }) => {
  const { js } = await request.json();
  let js_parsed;
  try {
    js_parsed = clone(JSON.parse(js));
  } catch (e) {
    js_parsed = { "message": "error" };
  }
  return json(js_parsed);
};
