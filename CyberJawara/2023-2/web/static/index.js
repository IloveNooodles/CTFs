const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

// const config = require('./config.js')

const server = http.createServer((req, res) => {
  if (req.url.startsWith('/static/')) {
    const urlPath = req.url.replace(/\.\.\//g, '');
    console.log(urlPath);
    const filePath = path.join(__dirname, urlPath);
    console.log(filePath);
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404);
        res.end('Error: File not found');
      } else {
        res.writeHead(200);
        res.end(data);
      }
    });
  } else if (req.url.startsWith('/admin/')) {
    const parsedUrl = url.parse(req.url, true);
    const queryObject = parsedUrl.query;
    if (queryObject.secret == config.secret) {
      res.writeHead(200);
      res.end(config.flag);
    } else {
      res.writeHead(403);
      res.end('Nope');
    }
  } else if (req.url == '/') {
    fs.readFile('index.html', (err, data) => {
      if (err) {
        res.writeHead(500);
        res.end('Error');
      } else {
        res.writeHead(200);
        res.end(data);
      }
    });
  } else {
    res.writeHead(404);
    res.end('404: Resource not found');
  }
});

server.listen(3000, () => {
  console.log('Server running at http://localhost:3000/');
});
