import { Application, Status } from "../../deps.ts";
import { RoutesHandler } from "../../utils/routes.handler.ts";
import { User } from "../../models/user.ts";

export const handler = (app: Application) => {
  new RoutesHandler(app, (router) => {
    router.post("/api/register", async (ctx) => {
      const body = ctx.request.body({ type: "json" });
      const value: User = await body.value;
      const user = ["username", "password"];
      const send = (res: { message: string; status: number }): void => {
        ctx.response.body = JSON.stringify({ message: res.message });
        ctx.response.status = res.status;
      };
      for (const prop of user) {
        if (!(prop in value)) {
          send({
            message: `${prop} not specified in request body`,
            status: Status.BadRequest,
          });
          return;
          ///@ts-ignore get property of type User
        } else if (value[prop] == "") {
          send({
            message: `${prop} cannot be empty`,
            status: Status.BadRequest,
          });
          return;
          ///@ts-ignore get property of type User
        } else if (value[prop].length < 5) {
          send({
            message: `${prop} too short`,
            status: Status.BadRequest,
          });
          return;
        }
      }
      ctx.state.session.set("user", value);
      send({
        message: "success",
        status: Status.Accepted,
      });
      return;
    });
  });
};
