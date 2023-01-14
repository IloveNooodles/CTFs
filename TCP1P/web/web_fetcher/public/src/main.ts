import { Application, Router } from "https://deno.land/x/oak@v10.5.1/mod.ts";
import {
  dejsEngine,
  oakAdapter,
  viewEngine,
} from "https://deno.land/x/view_engine@v10.5.1c/mod.ts";
import { Status } from "https://deno.land/std@0.170.0/http/http_status.ts";

const app = new Application();
const route = new Router();

app.use(
  viewEngine(oakAdapter, dejsEngine, {
    viewRoot: "./views",
  }),
);
route.get("/", (ctx) => {
  ctx.render("index.html", { title: "home", data: false });
});

route.post("/", async (ctx) => {
  const body = ctx.request.body({ type: "form" });
  const value = await body.value;
  const url = value.get("url");
  console.log(url);
  if (!url) {
    ctx.response.body = JSON.stringify({
      "message": "form url not found in request body",
    });
    ctx.response.status = Status.BadRequest;
  } else {
    await fetch(url).then(async (ok) => await ok.text())
      .then((data) => {
        ctx.render("index.html", { title: "home", data: data });
      })
      .catch((err) => {
        ctx.render("index.html", { title: "home", data: err });
      });
  }
});
app.use(route.routes());
app.use(route.allowedMethods());

if (import.meta.main) {
  const port = Number(Deno.env.get("PORT")) || 8080;
  console.log(Deno.env.get("PORT"))
  console.log(`run @ http://localhost:${port}`);
  await app.listen({ port: port });
}
