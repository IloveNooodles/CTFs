const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const crypto = require("crypto");
const { exec } = require('child_process');

const app = express();
const port = 3000;
const blacklist = ['REDACTED'];

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

function removeOldFiles(directory) {
    const now = Date.now();
    fs.readdir(directory, (err, files) => {
        if (err) throw err;
        files.forEach(file => {
            const filePath = path.join(directory, file);
            fs.stat(filePath, (err, stats) => {
                if (err) throw err;
                const fileAge = now - stats.mtimeMs;
                if (fileAge > 60 * 1000) { 
                    fs.unlink(filePath, (err) => {
                        if (err) throw err;
                        console.log(`Removed old file: ${filePath}`);
                    });
                }
            });
        });
    });
}

app.use("/static", express.static(__dirname + '/static'));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'static/index.html'));
});

app.post('/convert', upload.single('video'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file uploaded.' });
    }

    const inputBuffer = req.file.buffer;
    const content = inputBuffer.toString().toLowerCase();
    const originalFileName = req.file.originalname;
    
    if (originalFileName.includes(' ')) {
        return res.status(400).json({ error: 'Your filename contains whitespace' });
    }    
    const hasBlacklistKeywords = blacklist.some(keyword => originalFileName.toLowerCase().includes(keyword));
    if (hasBlacklistKeywords) {
        return res.status(400).json({ error: 'Say no to hacker' });
    }
    if (req.file.mimetype !== 'video/mp4') {
        return res.status(400).json({ error: 'Invalid file format' });
    }
    const fileExtension = path.extname(originalFileName).toLowerCase();

    if (fileExtension !== '.mp4') {
        return res.status(400).json({ error: 'Invalid file extension' });
    }

    if (req.file.size > 500000) {
        return res.status(400).json({ error: 'File too large', note: 'Limited only for 500kb' });
    }

    const randNameOutput = crypto.createHash('md5').update(crypto.randomBytes(16)).digest('hex');
    const outputFilePath = path.join(__dirname, `uploads/${randNameOutput}.mp3`);

    const inputFileTempPath = path.join(__dirname, `uploads/${originalFileName}.mp4`);
    fs.writeFileSync(inputFileTempPath, inputBuffer);

    const ffmpegCommand = `ffmpeg -i ${inputFileTempPath} -vn -ar 44100 -ac 2 -ab 192k -f mp3 "${outputFilePath}"`;
    exec(ffmpegCommand, (error, stdout, stderr) => {
        if (error) {
            console.error('Error during conversion:', error);
            res.status(500).json({ error: 'Error during conversion.' });
        } else {
            res.setHeader('Content-Disposition', 'attachment; filename=converted.mp3');
            res.setHeader('Content-Type', 'audio/mpeg');
            const fileStream = fs.createReadStream(outputFilePath);
            fileStream.on('end', () => {
                fs.unlinkSync(outputFilePath);
            });
            fileStream.pipe(res);
        }

        setInterval(() => {
            removeOldFiles(path.join(__dirname, 'uploads'));
        }, 60 * 1000); 

    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
