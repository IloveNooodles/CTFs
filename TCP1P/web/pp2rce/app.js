import { handler } from "./build/handler.js";
import { Server } from "http";
import express from "express";

const port = 8080;
const hostname = "localhost";

const app = express();
app.use(handler);
app.use((a)=>{
  console.log(a)
})
const http = new Server(app);

http.listen(port, () => {
  console.log(`TCP1P server running at http://${hostname}:${port}/`);
});
