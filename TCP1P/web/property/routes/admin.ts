import { Application, Status } from "../deps.ts";
import { User } from "../models/user.ts";
import { RoutesHandler } from "../utils/routes.handler.ts";

const FLAG = await Deno.readFile("flag.txt").then((uint) => {
  return new TextDecoder().decode(uint);
});

export const handler = (app: Application) => {
  new RoutesHandler(app, (router) => {
    router.get("/admin", (ctx) => {
      const user = ctx.state.session.get("user") as User;
      if (!user) {
        ctx.response.redirect("/register");
        return;
      }
      if (!user.isAdmin) {
        ctx.response.status = Status.Forbidden;
        return;
      }
      ctx.render("admin.html", { user: user, path: "/admin", flag: FLAG });
      return;
    });
  });
};
