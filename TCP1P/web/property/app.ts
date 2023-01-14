import {
  Application,
  AppState,
  DB,
  dejsEngine,
  oakAdapter,
  SqliteStore,
  viewEngine,
  walk,
  Session
} from "./deps.ts";

import * as config from "./config.ts";

interface AppInner {
  app: Application<AppState>;
  session_db: DB;
  session_store: SqliteStore;
}

export class App implements AppInner {
  app: Application<AppState>;
  session_db: DB;
  session_store: SqliteStore;
  port: number;

  constructor() {
    this.app = new Application<AppState>();
    this.session_db = new DB(config.DB_FILE_NAME);
    this.port = config.PORT;
    ///@ts-ignore session store init
    this.session_store = new SqliteStore(this.session_db);
    ///@ts-ignore session midleware
    this.app.use(Session.initMiddleware(this.session_store, {sessionCookieName:config.SESSION_COOKIE_NAME}));
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
        import(`./${path}`).then((module) => {
          module.handler(this.app);
        });
      }
    }
    console.log(`run @ http://localhost:${this.port}`);
    this.app.listen({ port: this.port });
  }
}
