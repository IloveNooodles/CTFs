import { URL, PORT } from "./config.js"
import express from "express"
import { visit } from "./helpers/robot.js"

const app = express()

app.set('view engine', 'ejs');
app.use("/static", express.static("static"))

app.get("/", (req, res) => {
    const { url } = req.query
    if (url) {
        visit(url)
    }
    res.render("index", {
        base: URL
    })
})

app.listen(PORT, () => {
    console.log(`listening @ ${URL}`)
})