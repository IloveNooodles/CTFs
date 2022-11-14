import puppeteer from 'puppeteer'
import express from 'express'
import rateLimit from 'express-rate-limit'

const app = express()
app.use(express.static('static'))
app.use(express.json())

const port = 7999
let url = ''
let browser

async function visit(url) {
    const ctx = await browser.createIncognitoBrowserContext()
    const page = await ctx.newPage()
    try {
        await page.goto(url, { timeout: 20 * 1000, waitUntil: 'load' })
    } catch (err){
        console.log(err);
    } finally {
        await page.close()
        await ctx.close()
    }

    console.log(`Done visiting -> ${url}`)
}

app.use(
    '/visit', rateLimit({
        windowMs: 30 * 1000,
        max: 10,
        message: { error: 'Too many requests, try again later' }
    })
)

app.get('/visit', async (req, res) => {
    let {url} = req.query
    res.setHeader("Content-Type", "application/json");
    
    if(
        (typeof url !== 'string') || (url === undefined) || 
        (url === '') || (!/^(http|https)?:\/\/(webapp:8000\/)/gi.test(url))
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
    console.log(`[*] Listening on port ${port}`)
})
