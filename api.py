import time
import math
import os
import string

from flask import Blueprint, request, redirect, make_response
from bcrypt import checkpw
import jwt

import DBHelper
from misc import error, host_limit, auth
from config import JWT_EXP

api = Blueprint(name="api", import_name=__name__)

# Users
@api.route("/login", methods = ["POST"])
@host_limit("panel")
def login():
    # arguments
    username = request.form.get("username")
    password = request.form.get("password")
    if (username is None) or (password is None):
        return error("Invalid arguments"), 400
    username, password = str(username), str(password)
    if (len(username) == 0) or (len(password) == 0): 
        return error("Invalid arguments"), 400
    
    # get user
    user = DBHelper.select_user_with_username(username)
    if user is None: 
        return error("Login failed"), 401
    
    # check password
    if checkpw(password.encode("utf-8"), user[1].encode("utf-8")):
        # jwt
        key = os.getenv("JWT_KEY", None)
        payload = {
            "user": username,
            "exp": math.floor(time.time()) + JWT_EXP
        }
        token = jwt.encode(payload=payload, key=key, algorithm="HS256")
        
        resp = make_response(redirect("/panel"))
        resp.set_cookie("token", token, httponly=True)
        return resp
    else:
        return error("Login failed!"), 401


@api.route("/register", methods = ["POST"])
@host_limit("panel")
def register():
    # arguments
    username = request.form.get("username")
    password = request.form.get("password")
    if (username is None) or (password is None):
        return error("Invalid arguments"), 400
    username, password = str(username), str(password)
    if (len(username) == 0) or (len(password) == 0): 
        return error("Invalid arguments"), 400
    
    # 確定是否有重複用戶
    result = DBHelper.select_user_with_username(username=username)
    if not(result is None):
        return error("User already exists!"), 400
    
    # 註冊
    DBHelper.insert_user(username=username, password=password)
    
    return redirect("/login")


# Lao 佬
@api.route("/page", methods=["POST"])
@host_limit("panel")
def new_page():
    opuser = auth()
    if opuser:
        # arguments
        subdomain = request.form.get("subdomain", None)
        color = request.form.get("color", None)
        name = request.form.get("name", None)
        if (subdomain is None) or (color is None) or (name is None):
            return error("Invalid arguments"), 400
        subdomain, color, name = str(subdomain), str(color), str(name)
        if (len(subdomain) == 0) or (len(name) == 0) or (len(color) != 7) or \
                (subdomain == "panel"): # subdomain 不能是 panel
            return error("Invalid arguments"), 400

        # check subdomain
        for _ in subdomain: # 檢查不合法字元
            if not(_ in (string.ascii_letters + string.digits + "-")):
                return error("Invalid subdomain"), 400
        if subdomain.startswith("-") or subdomain.endswith("-"):
            return error("Invalid subdomain"), 400
        # 檢查重複subdomain
        repeated = DBHelper.select_lao_with_subdomain(subdomain=subdomain)
        if repeated:
            return error("Subdomain is already exists"), 400

        # check color
        try:
            color = int(color[1:], 16)
        except:
            return error("Invalid color"), 400

        # insert
        DBHelper.insert_lao(subdomain=subdomain,
                            name=name,
                            color=color,
                            userhash=DBHelper.select_user_with_username(username=opuser)[2])
    
        return redirect("/panel")
    else:
        return redirect("/login")


@api.route("/delpage/<int:id>", methods=["GET"])
@host_limit("panel")
def del_page(id:int):
    opuser = auth()
    if opuser:
        opuser_userhash = DBHelper.select_user_with_username(username=opuser)[2]
        lao_userhash = DBHelper.select_lao_with_id(id=id)[0]
        if opuser_userhash == lao_userhash:
            DBHelper.delete_lao(lid=id)
            return redirect("/panel")
        else:
            return error("You don't have permission to visit this page."), 402
    else:
        return redirect("/login")