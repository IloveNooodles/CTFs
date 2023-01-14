import puppeteer, {
  type Page,
} from "https://deno.land/x/puppeteer@16.2.0/mod.ts";
import { DOMAIN } from "../config.ts";

const FLAG = await Deno.readFile("./flag.txt").then((val) => {
  return new TextDecoder().decode(val);
});

export async function visit(url: string) {
  console.log(url);
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      "--no-sandbox",
      "--disable-default-apps",
      "--disable-dev-shm-usage",
      "--disable-extensions",
      "--disable-gpu",
      "--disable-sync",
      "--disable-translate",
      "--hide-scrollbars",
      "--metrics-recording-only",
      "--mute-audio",
      "--no-first-run",
      "--safebrowsing-disable-auto-update",
    ],
  });
  let page: null | Page = await browser.newPage();

  try {
    await page.setCookie({
      name: "secret",
      value: FLAG,
      domain: DOMAIN,
      sameSite: "Lax",
      httpOnly: false,
      secure: false,
      sourceScheme: "NonSecure",
    });
    await page.goto(url, { waitUntil: "networkidle2" }).catch((e) =>
      console.log(e)
    );
    console.log(await page.cookies());
    await new Promise((resolve) => setTimeout(resolve, 500));
    console.log("admin is visiting url:");
    console.log(url);
    await page.close();

    console.log("admin visited url");
    page = null;
  } catch (err) {
    console.log(err);
  } finally {
    if (page) await page.close();
    console.log("page closed");
    if (browser) await browser.close();
    console.log("browser closed");
    //no reject
    console.log("resolved");
  }
}
