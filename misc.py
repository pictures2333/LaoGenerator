from functools import wraps
import os

from flask import request, jsonify, abort
import jwt

from config import DOMAIN
from DBHelper import select_user_with_username

def error(msg:str):
    return jsonify({"error":msg})


def host_limit(hostreq:str):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.host == f"{hostreq}.{DOMAIN}":
                return f(*args, **kwargs)
            return abort(404)
        return decorated_function
    return decorator


def auth() -> str | None:
    # jwt decode
    cookie = request.cookies.get("token", None)
    if cookie is None:
        return None
    
    try:
        user = jwt.decode(jwt = cookie, key = os.getenv("JWT_KEY", None), algorithms=["HS256"])
    except:
        return None
    
    # search db
    dbuser = select_user_with_username(username=user["user"])
    if dbuser is None:
        return None
    
    return dbuser[0]