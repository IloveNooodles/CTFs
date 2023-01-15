import express from "express";
import ejs from "ejs";

const PORT = process.env.PORT || 8080;
const app = express();

app.use(express.urlencoded({ extended: true }));

async function make_template(input) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const template = ejs.compile(`
            <html lang="en">
          
            <head>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet"
                    integrity="sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD" crossorigin="anonymous">
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"
                    integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN"
                    crossorigin="anonymous"></script>
                <title>home</title>
            </head>
            
            <body>
                <div class="container-fluid vh-100">
                    <div class="row h-100 d-flex justify-content-center align-items-center">
                        <div class="col-lg-6 col-md-8 col-sm-10 col-s border-dark rounded-3 shadow-lg bg-white">
                            <form action="/" method="get">
                                <div class="container-fluid">
                                    <div class="d-flex justify-content-center border-bottom">
                                        <h2>Echoers</h2>
                                    </div>
                                    <div class="p-3">
                                        <input type="input" class="form-control" name="input" id="input" placeholder="hello world"
                                            required>
            
                                        <div class="d-flex my-3">
                                            <input type="reset" value="Erase" class="btn btn-danger w-50"
                                                onclick="document.getElementById('output').innerHTML = ''">
                                            <input type="submit" value="Send" class="btn btn-primary w-50" onclick="send()">
                                        </div>
                                        <div class="card mt-3">
                                            <div class="card-body">
                                                <p id="output">${input}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"
                    integrity="sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN"
                    crossorigin="anonymous"></script>
            </body>
            
            </html>
              `)();
      resolve(template);
    }, 1000);
  });
}

app.get("/", async (req, res) => {
  const input = req.query.input || "";
  const template = await make_template(input)
  return res.send(template);
});

app.listen(PORT, () => {
  console.log(`listening @ http://localhost:${PORT}`);
});
