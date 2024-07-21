from flask import Flask, render_template, render_template_string

app = Flask(__name__)

def filter(string):
    blacklist = ["\"", "'", "`", "|", " ", "[", "]", "+", "init", "subprocess", "config", "update", "mro", "subclasses", "class", "base", "builtins"]
    for word in blacklist:
        if word in string:
            return False
    return True
    
idols = {
    "hinana" : {
        "name": "Hinana Ichikawa",
        "fullname": "市川雛菜 (Ichikawa Hinana)",
        "age": "15",
        "height": "165cm",
        "weight": "56 kg",
        "birthday": "March 17th",
        "blood_type": "A",
        "hobbies": "I like everything just fine~",
        "skills": "I can do anything just fine~",
        "picture": "https://image.shinycolors.wiki/a/a9/HinanaProfile.png"
    },
    "toru" : {
        "name": "Toru Asakura",
        "fullname": "浅倉透 (Asakura Tooru)",
        "age": "17",
        "height": "160cm",
        "weight": "50 kg",
        "birthday": "May 4th",
        "blood_type": "B",
        "hobbies": "Watching movies and dramas",
        "skills": "Remembering people's faces",
        "picture": "https://image.shinycolors.wiki/2/2d/ToruProfile.png"
    },
    "madoka" : {
        "name": "Madoka Higuchi",
        "fullname": "樋口 円香 (Higuchi Madoka)",
        "age": "17",
        "height": "159cm",
        "weight": "47 kg",
        "birthday": "October 27th",
        "blood_type": "B",
        "hobbies": "Not really anything",
        "skills": "Not really anything",
        "picture": "https://image.shinycolors.wiki/9/91/MadokaProfile.png"
    },
    "koito" : {
        "name": "Koito Fukumaru",
        "fullname": "福丸小糸 (Fukumaru Koito)",
        "age": "16",
        "height": "148cm",
        "weight": "42 kg",
        "birthday": "November 11th",
        "blood_type": "O",
        "hobbies": "Reading",
        "skills": "Study",
        "picture": "https://image.shinycolors.wiki/8/85/KoitoProfile.png"
    },
}

@app.route('/')
def index():
    render = render_template('index.html')
    return render_template_string(render)

@app.route('/<idol>')
def detail(idol):
    try :
        idol = idol.lower()
        render = render_template('idol.html', data=idols[idol])
        return render_template_string(render)
    except :
        try:
            if(not filter(idol)):
                return render_template('invalid.html')
            render = render_template('404.html', idol=idol)
            return render_template_string(render)
        except:
            return "Internal server error"

if __name__ == '__main__':
    app.run(debug=True)