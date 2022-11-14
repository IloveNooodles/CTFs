import express from 'express'
import fs from 'fs'
import axios from 'axios';
import rateLimit from 'express-rate-limit'

const index = fs.readFileSync("./html/index.html").toString();
const app = express();
const port = 8001

function rand(length) {
    var result           = '';
    var characters       = 'abcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

app.use('/static', express.static('static'));
app.use(
    '/report', rateLimit({
        windowMs: 30 * 1000,
        max: 10,
        message: { error: 'Too many requests, try again later' }
    })
)

app.get('/', function(req, res){
	res.setHeader("Content-Type","text/html");
	res.send(index.replace(/{{nonce}}/g, rand(16)));
});

app.get('/report', async function (req, res) {
    let {url} = req.query
    res.setHeader("Content-Type", "application/json");

    if(
        (typeof url !== 'string') || (url === undefined) || 
        (url === '') || (!/^(http|https)?:\/\//gi.test(url))
    ){
        return res.status(400).send({error: "Invalid url"})
    }

    try {
        await axios.get(`http://worker:7999/visit?url=${encodeURIComponent(url)}`).then((r) => {
            return res.status(200).send({ msg: r.data })
        })
    } catch (e) {
        console.error(`[-] Error visiting ${url}: ${e.message}`)
        return res.status(400).send({ error: e.message })
    }
});

app.listen(port, async () => {
    console.log(`[*] Webapp Listening on port ${port}`)
})

