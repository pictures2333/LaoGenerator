import hashlib
import time

from bcrypt import hashpw, gensalt
import sqlite3

# users
def select_user_with_username(username:str) -> tuple | None:
    db = sqlite3.connect("./db/lao.db")
    c = db.cursor()
    cursor = c.execute("SELECT username,password,hash FROM user WHERE username=?", (username,)).fetchone()
    return cursor


def insert_user(username:str, password:str) -> None:
    pwha = hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")
    userhash = hashlib.sha256( (username+str(time.time())).encode() ).hexdigest()
    
    db = sqlite3.connect("./db/lao.db")
    c = db.cursor()
    c.execute("INSERT INTO user (username, password, hash) VALUES (?, ?, ?)", (username, pwha, userhash))
    db.commit()
    

# laos
def select_lao_with_subdomain(subdomain:str) -> tuple | None:
    db = sqlite3.connect("./db/lao.db")
    c = db.cursor()
    cursor = c.execute("SELECT subdomain,name,color,userhash FROM laotable WHERE subdomain=?", (subdomain,)).fetchone()
    return cursor


def select_lao_with_userhash(userhash:str) -> list | None:
    db = sqlite3.connect("./db/lao.db")
    c = db.cursor()
    cursor = c.execute("SELECT subdomain,name,color,id FROM laotable WHERE userhash=?", (userhash,)).fetchall()
    return cursor


def select_lao_with_id(id:int) -> tuple | None:
    db = sqlite3.connect("./db/lao.db")
    c = db.cursor()
    cursor = c.execute("SELECT userhash FROM laotable WHERE id=?", (id,)).fetchone()
    return cursor
    

def insert_lao(subdomain:str, color:int, name:str, userhash:str) -> None:
    db = sqlite3.connect("./db/lao.db")
    c = db.cursor()
    c.execute("INSERT INTO laotable (subdomain, name, color, userhash) VALUES (?, ?, ?, ?)", (subdomain, name, color, userhash))
    db.commit()
    

def delete_lao(lid:int) -> None:
    db = sqlite3.connect("./db/lao.db")
    c = db.cursor()
    c.execute("DELETE FROM laotable WHERE id=?", (lid,))
    db.commit()