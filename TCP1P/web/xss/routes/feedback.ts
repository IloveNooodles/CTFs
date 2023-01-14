import { Application, Status } from "../deps.ts";
import { RoutesHandler } from "../utils/routes.handler.ts";
import { visit } from "../helpers/robot.ts";

export const handler = (app: Application) => {
  new RoutesHandler(app, (router) => {
    router.get("/feedback", (ctx) => {
      ctx.render("feedback.html");
    });
    router.post("/feedback", async (ctx) => {
      const param = await ctx.request.body({ type: "form" }).value;
      const url = param.get("url");
      if (!url) {
        ctx.response.body = JSON.stringify({
          message: "url parameter not found in request body",
        });
        ctx.response.status = Status.BadRequest;
        return;
      }
      try {
        await visit(url);
        ctx.response.body = JSON.stringify({
          message: "success",
        });
        ctx.response.status = Status.OK;
        return;
      } catch (e) {
        console.log(e);
        ctx.response.body = JSON.stringify({
          message: "robot can't access the url",
        });
        ctx.response.status = Status.BadRequest;
        return;
      }
    });
  });
};
