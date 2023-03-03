const express        = require('express');
const router         = express.Router();
const uid            = require('../helper/uid');
const url_handler    = require('../helper/url_handler');
const bot            = require('../helper/bot');

let db;

const response = data => ({ message: data });

router.get('/', (req, res) => {
	return res.render('index.html');
});

router.get('/:id', (req, res) => {
    try {
        db.getPaste(req.params.id)
        .then((data) => {
            if (data) {
                return res.render('paste.html');
            }
            return res.status(404).send(response('404 page not found'));
        })
        .catch(() => res.status(404).send(response('An error occurred')));
    } catch (error) {
        return res.status(500).send(response('Internal server error'));
    }
})

router.get('/api/paste/:id', (req, res) => {
    try {
        db.getPaste(req.params.id)
        .then((data) => {
            if (data) {
                const paste = url_handler.makeHyperLink(data.value);
                return res.send({
                    "value": paste
                });
            }
            return res.status(404).send(response('404 page not found'));
        })
        .catch(() => res.status(404).send(response('An error occurred')));
    } catch (error) {
        return res.status(500).send(response('Internal server error'));
    }
})

router.post('/api/report', async (req, res) => {
    try {
        const { id } = req.body;
        if (id) {
            await bot.reportPaste(id)
            .then(() => res.send({
                "message": "Paste reported. Admin will check it soon.",
                "success": "true"
            }))
            .catch(() => res.status(404).send(response('An error occurred')));
        } else {
            return res.status(401).send(response('Please fill out all the required fields!'));
        }
    } catch (error) {
        return res.status(500).send(response('Internal server error'));
    }
})

router.post('/', async (req, res) => {
    try {
        const { paste } = req.body;

        if (paste) {
            const id = uid.generate();
            return db.newPaste(id, paste)
                .then(() => res.send({ id: id }))
                .catch(() => res.send(response('Something went wrong!')));
        }
        return res.status(401).send(response('Please fill out all the required fields!'));
    } catch (error) {
        return res.status(500).send(response('Internal server error'));
    }
});

module.exports = database => { 
	db = database;
	return router;
};