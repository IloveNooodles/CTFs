import { exec } from "child_process";

import type * as kit from "@sveltejs/kit";

export const handle: kit.Handle = async ({ event, resolve }) => {
  const response = await resolve(event);
  exec(`echo last accessed @ ${Date.now()} > log.txt`);
  return response;
};

export const handleError: kit.HandleServerError = ({ error, event }) => {
  //@ts-ignore
  const message = error.message;
  return {
    message,
  };
};
