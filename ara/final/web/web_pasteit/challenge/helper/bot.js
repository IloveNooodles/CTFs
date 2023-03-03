const puppeteer = require('puppeteer');

const browser_options = {
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
		'--js-flags=--noexpose_wasm,--jitless'
	]
};

const cookies = [{
	'name': 'flag',
	'value': '[REDACTED]'
}];

const reportPaste = async (id) => {
    try {
		const browser = await puppeteer.launch(browser_options);
		let context = await browser.createIncognitoBrowserContext();
		let page = await context.newPage();
		await page.goto('http://localhost:1339/');
		await page.setCookie(...cookies);
		await page.goto(`http://localhost:1339/${id}`, {
			waitUntil: 'networkidle2'
		});
        await page.waitForTimeout(2000);
		await browser.close();
    } catch(e) {
        console.log(e);
    }
};

module.exports = { reportPaste };