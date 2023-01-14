import { Application } from "./deps.ts";
import { walk } from "./deps.ts";
import { dejsEngine, oakAdapter, viewEngine } from "./deps.ts";
import { DOMAIN, PORT } from "./config.ts";

interface AppInner {
  app: Application;
}

export class App implements AppInner {
  app: Application;

  constructor() {
    this.app = new Application();
    this.app.use(
      viewEngine(oakAdapter, dejsEngine, {
        viewRoot: "./views",
      }),
    );
  }

  async init() {
    for await (const file of walk("./routes/")) {
      const path = file.path;
      if (path.endsWith(".ts")) {
        await import(`./${path}`).then((module) => {
          module.handler(this.app);
        });
      }
    }
    console.log(`run @ http://${DOMAIN}:${PORT}`);
    this.app.listen({ port: PORT});
  }
}

