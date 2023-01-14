export const PORT = Number(Deno.env.get("PORT")) || 8080;
export const DB_FILE_NAME = Deno.env.get("DB_FILE_NAME") || "session.db";
export const SESSION_COOKIE_NAME = Deno.env.get("SESSION_COOKIE_NAME") || "local_session"