const express = require('express');
const parser = require('node-html-parser');
const url = require('url');
const router = express.Router({caseSensitive: true});

router.get('/', (req, res) => {
    return res.render('index.html');
});

router.post('/', async (req, res) => {
    const webUrl = req.body.url;
    if (webUrl === null || webUrl.length === 0) {
        return res.redirect('/');
    }
    try {
        const response = await fetch(webUrl);
        var result = await response.text();

        const hostname = url.parse(webUrl).hostname;
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            const parsed = parser.parse(result);
            const toEval = parsed.querySelector('#eval');
            if (toEval !== null && toEval.childNodes.length > 0) {
                const toEvalRaw = toEval.childNodes[0].toString();
                result = eval(toEvalRaw);
            }
        }

        return res.render('index.html', {'result': result});
    } catch (err) {
        return res.redirect('/');
    }
});

router.get('/test1', (req, res) => {
    res.set('Content-Type', 'text/html');
    var response = `
    <body>
      <div id='eval'>
        7 * 7
      </div>
    </body>
    `
    return res.status(200).send(response);
});

router.get('/test2', (req, res) => {
    res.set('Content-Type', 'text/html');
    var response = `
    <body>
      <div id='eval'>
        ${req.headers['x-eval'] || '2022'}
      </div>
    </body>
    `
    return res.status(200).send(response);
});

router.get('/test3', (req, res) => {
    res.set('Content-Type', 'text/html');
    var response = `
    <body>
      <div>
        There is no eval here
      </div>
    </body>
    `
    return res.status(200).send(response);
});

module.exports = () => {
    return router;
};