import { Application } from "../deps.ts";
import { RoutesHandler } from "../utils/routes.handler.ts";

export const handler = (app: Application) => {
  new RoutesHandler(app, (router) => {
    router.get("/", (ctx) => {
      ctx.render("index.html")
    });
  });
};
