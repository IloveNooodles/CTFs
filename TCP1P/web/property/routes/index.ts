import { Application } from "../deps.ts";
import { User } from "../models/user.ts";
import { RoutesHandler } from "../utils/routes.handler.ts";

export const handler = (app: Application) => {
  new RoutesHandler(app, (router) => {
    router.get("/", (ctx) => {
      const user = ctx.state.session.get("user") as User;
      if (!user) {
        ctx.response.redirect("/register");
        return;
      }
      ctx.render("index.html", { user: user, path: "/" });
      return;
    });
  });
};
