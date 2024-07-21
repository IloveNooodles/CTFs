const express = require('express');
const app = express();
const nunjucks = require('nunjucks');
const routes = require('./routes/routes');
const bodyParser = require("body-parser");

app.use(bodyParser.urlencoded({extended: true}));

nunjucks.configure("views", {
    autoescape: true,
    express: app,
    views: "templates",
});

app.use(routes());

app.all('*', (req, res) => {
    return res.status(404).send(`Path ${req.path} not found`);
});

(async() => {
    app.listen(1337, '0.0.0.0', () => console.log('Listening on port 1337'));
})();