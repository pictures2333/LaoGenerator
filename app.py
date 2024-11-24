import os

from flask import Flask, request, render_template, abort, redirect, url_for, make_response
# from dotenv import load_dotenv

from api import api
from config import DOMAIN
from misc import host_limit, auth
import DBHelper

# load_dotenv()

# app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
# blueprint
app.register_blueprint(api, url_prefix="/api")

# index
@app.route("/")
def index():
    if request.host == f"panel.{DOMAIN}":
        return redirect(url_for("panel"))
    
    subdomain = request.host.replace(f".{DOMAIN}", "")
    result = DBHelper.select_lao_with_subdomain(subdomain)
    if result is None:
        return abort(404)
    return render_template("lao.html", subdomain=result[0], name=result[1], color=hex(result[2])[2:])

# panel
@app.route("/panel", methods = ["GET"])
@host_limit("panel")
def panel():
    user = auth()
    if user:
        userhash = DBHelper.select_user_with_username(user)[2]
        laos = DBHelper.select_lao_with_userhash(userhash=userhash)
        laos = [ (f"{l[0]}.{DOMAIN}", l[1], hex(l[2])[2:], str(l[3])) for l in laos ]
        return render_template("panel.html", user = user, laos = laos)
    
    return redirect("/login")
    

# login / register
@app.route("/login", methods = ["GET"])
@host_limit("panel")
def login():
    if auth():
        return redirect("/panel")
    else:
        return render_template("login.html", type = 1)
@app.route("/register", methods = ["GET"])
@host_limit("panel")
def register():
    if auth():
        return redirect("/panel")
    else:
        return render_template("login.html", type = 2)
@app.route("/logout", methods = ["GET"])
@host_limit("panel")
def logout():
    resp = make_response(redirect("/panel"))
    resp.set_cookie("token", "")
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=False)