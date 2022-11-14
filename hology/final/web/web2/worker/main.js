import puppeteer from 'puppeteer'
import express from 'express'

const app = express()
app.use(express.static('static'))
app.use(express.json())

const port = 7999
let browser
const now = ()=>Math.floor(Date.now() / 1000);
async function visit(url) {
    const ctx = await browser.createIncognitoBrowserContext()
    const page = await ctx.newPage()
    try {
        await page.setCookie({
			name: 'FLAG',
			value: process.env.FLAG || "flag{tesflag}",
			domain: "webapp",
            expires: now() + 100,
		});
        await page.goto(url, { timeout: 2 * 1000, waitUntil: 'networkidle2' })
        await page.waitForTimeout(10 * 1000)
    } catch (err){
        console.log(err);
    } finally {
        await page.close()
        await ctx.close()
    }

    console.log(`Done visiting -> ${url}`)
}

app.get('/visit', async (req, res) => {
    let {url} = req.query
    if(
        (typeof url !== 'string') || (url === undefined) || 
        (url === '') || (!/^(http|https)?:\/\//gi.test(url))
    ){
        return res.status(400).send({error: "Invalid url"})
    }
    
    try {
        console.log(`[*] Visiting ${url}`)
        await visit(url)
        console.log(`[*] Done visiting ${url}`)
        return res.sendStatus(200)
    } catch (e) {
        console.error(`[-] Error visiting ${url}: ${e.message}`)
        return res.status(400).send({ error: e.message })
    }
})

app.listen(port, async () => {
    browser = await puppeteer.launch({
        pipe: true,
        dumpio: true,
        ignoreHTTPSErrors: true,
        acceptInsecureCerts: true,
        headless: true,
        args: [
            '--no-sandbox',
            '--disable-background-networking',
            '--disable-default-apps',
            '--disable-extensions',
            '--disable-gpu',
            '--disable-sync',
            '--disable-translate',
            '--hide-scrollbars',
            '--metrics-recording-only',
            '--mute-audio',
            '--no-first-run',
            '--safebrowsing-disable-auto-update',
            '--disable-dev-shm-usage',

            '--ignore-certificate-errors',
            '--ignore-certificate-errors-spki-list'
        ]
    })
    console.log(`[*] Worker Listening on port ${port}`)
})