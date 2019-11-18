import os
from flask import Flask, render_template as template, session, url_for, request, redirect, json
app = Flask(__name__)
app.secret_key = os.urandom(8)
# Gera stuff tilbúið
teljari = 0
def getQuizzes():
    with open("static/quiz.json", "r", encoding="UTF-8") as f:
        quizzes = json.load(f)
        quizzes = quizzes["quizzes"]
        return quizzes
# -----------------
def addQuiz(spurningar,nafn):
    with open("static/quiz.json","r+", encoding="UTF-8") as f:
        data = json.load(f)
        print(spurningar)
        f.seek(0)
        f.truncate()
        data["quizzes"][nafn] = spurningar
        json.dump(data, f, indent=1,encoding="UTF-8")
quizzes = getQuizzes()
@app.route("/") # Root Routeið
def home():
    quizzes = getQuizzes()
    if "svor" in session: # Resettar cookies í hvert sinn sem þú ferð á root
        session.pop("svor")
        session.pop("teljari")
    return template("index.html",quizzes=quizzes)

@app.route("/quiz/<name>")
def quiz(name): # Gefur quiz eftir vali
    teljari = 0 # Redefinear teljara
    svor = {}
    if "teljari" in session: # Ef teljari er í session þá er hann notaður
        teljari = session["teljari"]
    else: # Ef ekki þá er hann settur inn í session
        session["teljari"] = teljari
    
    if "svor" in session: # Sama og með teljara
        svor = session["svor"]
    else:
        session["svor"] = svor

    return template("quiz.html",spurning = quizzes[name][teljari], quiznafn=name)

@app.route("/next/<name>", methods=["post"]) # Næsta spurning (hækkar teljara um eitt)
def next(name):
    svar = request.form["svar"]
    svor = {}
    rett = 0
    teljari = 0
    if "svor" in session:
        svor = session["svor"]
    else:
        session["svor"] = svor
    if "teljari" in session: # Notar teljara inn í session ef hann er til
        teljari = session["teljari"]
        svor[quizzes[name][teljari][1]] = [quizzes[name][teljari][2], svar] # setur spurningu, rétta svarið og giskaða svarið í dictionary með session
        if "rett" in session: # Notar rétt teljaran í session ef hægt
            rett = session["rett"]
        if "svor" in session:
            session["svor"] = svor
        else:
            svor = session["svor"]
        svor[quizzes[name][teljari][1]] = [quizzes[name][teljari][2], svar] # setur spurningu, rétta svarið og giskaða svarið í dictionary með sessions
        templisti = svor[quizzes[name][teljari][1]]
        if templisti[0].lower() == templisti[1].lower():
                rett += 1 # Hækkar rétt teljara um eitt ef svarið er rétt
        if teljari >= len(quizzes[name])-1:
            # ef spurningarnar eru búnar fer þetta í results
            session["rett"] = rett
            return redirect(f"/results/{name}")
        else:
            teljari += 1
        session["teljari"] = teljari
        session["rett"] = rett
        
    else: # Ef það er enginn teljari inn í Session þá gerist ekkert
        return redirect("/")
    
    return redirect(f"/quiz/{name}")


@app.route("/results/<name>")
def result(name): # Result fyrir spurningarnar
    if "svor" in session and "rett" in session:
        svor = session["svor"]
        rett = session["rett"]
    else:
        # engin svör voru sett í sessionið svo hér hefur eitthvað farið úrskeiðis
        # kannski /results skrifað beint inn í browser
        # redirectum bara á index eða eitthvað
        return redirect(url_for("home"))

    session.pop("svor")
    session.pop("teljari")
    session.pop("rett")
    return template("result.html", svor=svor, rett=rett, total = len(quizzes[name]))

@app.route("/nyttquiz", methods = ["POST","GET"])
def nytt():
    if request.method == "POST":
        max = int(request.form["max"])
        spurningar = []
        nafn = request.form["nafn"]
        for i in range(1,max+1):
            spurningar.append(
                [i, request.form["spurning"+str(i)], request.form["svar"+str(i)]]
            )
        addQuiz(spurningar,nafn)
        return "uwu"
    else:
        return template("nyttquiz.html")
@app.errorhandler(404)
def pagenotfound(error):
    return template("404.html"), 404

if __name__ == '__main__':
    #app.run()
    app.run(debug=True, use_reloader=True)