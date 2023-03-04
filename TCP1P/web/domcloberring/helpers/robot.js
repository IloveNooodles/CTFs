import puppeteer from "puppeteer";
import { URL } from "../config.js";
import { readFileSync } from "fs"

const FLAG = readFileSync("./flag.txt", 'utf-8')

export async function visit(url) {
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
    let page = await browser.newPage();

    try {
        const [domain, _port] = URL.replace("http://", "").split(":")
        await page.setCookie({
            name: "secret",
            value: FLAG,
            domain: 'localhost',
            sameSite: "Lax",
            httpOnly: false,
            secure: false,
            sourceScheme: "NonSecure",
        });
        await page.goto(url, { waitUntil: "networkidle2" }).catch((e) =>
            console.log(e)
        );
        await new Promise((resolve) => setTimeout(resolve, 5000));
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