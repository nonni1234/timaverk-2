import os
from flask import Flask, render_template as template, session, url_for, request, redirect, json
app = Flask(__name__)
app.secret_key = os.urandom(8)
# Gera stuff tilbúið
teljari = 0
with open("static/quiz.json", "r", encoding="UTF-8") as f:
    quizzes= json.load(f)
    quizzes = quizzes["quizzes"]
# -----------------

@app.route("/") # Root Routeið
def home():
    return template("index.html")

@app.route("/quiz/<name>")
def quiz(name):
    teljari = 0 # Redefinear teljara
    if "teljari" in session: # Ef teljari er í session þá er hann notaður
        teljari = session["teljari"]
    else: # Ef ekki þá er hann settur inn í session
        session["teljari"] = teljari

    return template("quiz.html",spurning = quizzes[name][teljari], quiznafn=name)


@app.route("/next/<name>") # Næsta spurning (hækkar teljara um eitt)
def next(name):
    if "teljari" in session: # Notar teljara inn í session ef hann er til
        teljari = session["teljari"]
        if teljari >= len(quizzes["shrek"])-1:
            # ef spurningarnar eru búnar fer þetta í results sem verður einhvernveginn
            # þetta er það eina sem ég er búin að gera ég kann ekki owo
            return redirect("/results")
        else:
            teljari += 1
        session["teljari"] = teljari
        
    else: # Ef það er enginn teljari inn í Session þá gerist ekkert
        pass
    return redirect("/quiz/%s" % name)

    



@app.errorhandler(404)
def pagenotfound(error):
    return template("404.html"), 404

if __name__ == '__main__':
    #app.run()
    app.run(debug=True, use_reloader=True)