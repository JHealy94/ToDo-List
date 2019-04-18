from flask import render_template, flash, url_for, redirect, request,jsonify
from todo import app, db, bcrypt
from todo.model import User, List, ListItem
from flask_login import login_user, logout_user, current_user, login_required
from todo.helpers import sendEmail, getUserFromCode

@app.route("/api/testing")
@login_required
def testing():
    return render_template('testing.html')

@app.route("/api/test")
def maketestingUser():
    user = User.query.filter_by(email="test@example.com").first()
    if user:
        login_user(user)
        return redirect(url_for('testing'))
    hashed_password = bcrypt.generate_password_hash("test").decode('utf-8')
    new_token = bcrypt.generate_password_hash(hashed_password)
    user = User(name="test", email="test@example.com", password=hashed_password, token=new_token)
    db.session.add(user)
    db.session.commit()
    flash('Your account has been created! You can now login', 'success')
    login_user(user)
    return redirect(url_for('testing'))

@app.route("/api/newlist/<name>")
@login_required
def newList(name="newist"):
    newList = List(title=name, user_id=current_user.id, author=current_user)
    db.session.add(newList)
    db.session.commit()
    #print(f"make new list named {newList.id}")
    return f"{newList.id}"

@app.route("/api/deleteList/<listId>")
@login_required
def deleteList(listId):
    L = List.query.filter_by(id=listId).first()
    items = ListItem.query.filter_by(list_id=listId)
    for item in items:
        #print(f"delete Item :{item} from list: {listId}")
        db.session.delete(item)
    db.session.delete(L)
    db.session.commit()
    #print(f"delete list with id:{listId}")
    return f"ok"

@app.route("/api/lists")
@login_required
def getLists():
    lists = List.query.filter_by(author=current_user)
    return jsonify([e.serialize() for e in lists])

@app.route("/api/newItem/<listid>/<item>")
@login_required
def newItem(listid,item):
    editing = List.query.filter_by(id=listid).first()
    new = ListItem(list_id=listid, content=item, list=editing)
    db.session.add(new)
    db.session.commit()
    #print(f"make item '{item}' in list :{listid}")
    return url_for("getLists")

@app.route("/api/deleteItem/<listId>/<itemId>")
def deleteItem(listId,itemId):
    I = ListItem.query.filter_by(list_id=listId,id=itemId).first()
    #print(I)
    db.session.delete(I)
    db.session.commit()
    #print(f"delete Item :{itemId} from list: {listId}")
    return f"ok"


