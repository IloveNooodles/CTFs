'use strict';

const express = require('express');
const puppeteer = require('puppeteer');

const PORT = 3000;
const HOST = '0.0.0.0';
const DOMAIN = "IP_SERVER:PORT";

async function visit(url){
  const browser = await puppeteer.launch(
    {
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
  );

  console.log("Try visit");
  const page = await browser.newPage();
  
  page.setCookie({
    'name': "flag",
    'value': "PLACEHOLDER_VALUE",
    'domain': DOMAIN
  });

  try {
    await page.goto(url, {waitUntil: 'networkidle0'});
    console.log("Visit " + url + " SUCCESS");
  }
  catch (e){
    console.log("Visit " + url + " ERROR");
  }
  console.log("browser close");
  await browser.close();
}

const app = express();

app.get('/', (req, res) => {
  var url = req.query.url;
  if (url){
    if (url.startsWith("http") && url.length <= 100){
      visit(url);
      res.send("visit process");
    }
    else{
      res.send("only accept http and certain length of url");
    }

  }
  else{
    res.send("no visit")
  }
});

app.listen(PORT, HOST, () => {
  console.log(`Running on http://${HOST}:${PORT}`);
});