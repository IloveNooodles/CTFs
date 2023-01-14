import { App } from "./app.ts";

if (import.meta.main) {
  await new App().init();
}
