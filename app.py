import os
from flask import Flask, render_template as template, url_for, request, redirect, json, make_response
app = Flask(__name__)
# Gera stuff tilbúið
teljari = 0
with open("static/quiz.json", "r", encoding="UTF-8") as f:
    quizzes= json.load(f)
    quizzes = quizzes["quizzes"]
# -----------------

@app.route("/") # Root Routeið
def home():
    # if "svor" in session:
    #     session.pop("svor")
    #     session.pop("teljari")
    
    if request.cookies.get("svor"): # Resettar cookies í hvert sinn sem þú ferð á root
        res = make_response(template("index.html",quizzes=quizzes))
        res.set_cookie("Kaka","kaka",max_age=0)
        res.set_cookie("svor","svor", max_age=0)
        res.set_cookie("teljari","teljari",max_age=0)
        res.set_cookie("ready","no",max_age=0)
        return res

    return template("index.html",quizzes=quizzes)


@app.route("/quiz/<name>")
def quiz(name): # Gefur quiz eftir vali
#if not request.cookies.get("ready"):
    teljari = "0" # Redefinear teljara
    svor = {}
    res = make_response(redirect(f"/{name}"))
    #if request.cookies.get("teljari"): # Ef teljari er í session þá er hann notaður
        #teljari = int(request.cookies.get("teljari"))
    #else: # Ef ekki þá er hann settur inn í session
    #if request.cookies.get("svor"): # Sama og með teljara
        #svor = dict(eval(request.cookies.get("svor")))
    #else:
        #res.set_cookie("svor",str(svor))
    res.set_cookie("ready","yes")
    res.set_cookie("teljari",str(teljari))
    res.set_cookie("svor",str(svor))
    return res
@app.route("/<name>")
def quizready(name):
    teljari = int(request.cookies.get("teljari"))
    svor = dict(eval(request.cookies.get("svor")))
    return template("quiz.html",spurning = quizzes[name][teljari], quiznafn=name, teljari=teljari)
@app.route("/next/<name>", methods=["post"]) # Næsta spurning (hækkar teljara um eitt)
def next(name):
    svar = request.form["svar"]
    svor = {}
    rett = 0
    teljari = 0
    res = make_response(redirect(f"/quiz/{name}"))

    if request.cookies.get("svor"):
        svor = dict(eval(request.cookies.get("svor")))
    else:
        res.set_cookie("svor",str(svor))

    if request.cookies.get("teljari"): # Notar teljara inn í session ef hann er til
        teljari = int(request.cookies.get("teljari"))
        svor[quizzes[name][teljari][1]] = [quizzes[name][teljari][2], svar] # setur spurningu, rétta svarið og giskaða svarið í dictionary með session
        if request.cookies.get("rett"): # Notar rétt teljaran í session ef hægt
            rett = int(request.cookies.get("rett"))
        if request.cookies.get("svor"):
            res.set_cookie("svor",str(svor))
        else:
            svor = dict(eval(request.cookies.get("svor")))
        svor[quizzes[name][teljari][1]] = [quizzes[name][teljari][2], svar] # setur spurningu, rétta svarið og giskaða svarið í dictionary með sessions
        templisti = svor[quizzes[name][teljari][1]]
        if templisti[0].lower() == templisti[1].lower():
                rett += 1 # Hækkar rétt teljara um eitt ef svarið er rétt
        if teljari >= len(quizzes[name])-1:
            # ef spurningarnar eru búnar fer þetta í results
            res.set_cookie("rett",str(rett))
            return redirect(f"/results/{name}")
        else:
            teljari += 1
        res.set_cookie("teljari",str(teljari))
        res.set_cookie("rett",str(rett))
        
    else: # Ef það er enginn teljari inn í Session þá gerist ekkert
        return redirect("/")
    
    return res


@app.route("/results/<name>")
def result(name): # Result fyrir spurningarnar
    if request.cookies.get("svor") and request.cookies.get("rett"):
        svor = dict(eval(request.cookies.get("svor")))
        rett = int(request.cookies.get("rett"))
        res = make_response(template("result.html", svor=svor, rett=rett, total = len(quizzes[name])))
    else:
        # engin svör voru sett í sessionið svo hér hefur eitthvað farið úrskeiðis
        # kannski /results skrifað beint inn í browser
        # redirectum bara á index eða eitthvað
        return redirect(url_for("home"))

    res.set_cookie("svor","svor", max_age=0)
    res.set_cookie("teljari","teljari", max_age=0)
    res.set_cookie("rett","ret", max_age=0)
    return res

@app.route("/cookie")
def cookie():
    if not request.cookies.get("Kaka"):
        res = make_response("Set inn cookie")
        listi = ["1","2","3"]
        res.set_cookie("Kaka",str(listi), max_age = 10)
    else:
        #res = make_response("Kakan er með value {}".format(request.cookies.get("Kaka")))
        listi = request.cookies.get("Kaka")
        res = make_response(template("cookie.html",cookie=list(eval(listi))))
    
    return res



@app.errorhandler(404)
def pagenotfound(error):
    return template("404.html"), 404

if __name__ == '__main__':
    #app.run()
    app.run(debug=True, use_reloader=True)