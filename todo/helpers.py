import os
import secrets
from todo import app
from PIL import Image
from flask_mail import Message
from todo import mail
from todo.model import User, List, ListItem


def sendEmail(email):
   msg = Message('Password Reset For ListIt', sender = 'raspberrypi.gaylord@gmail.com', recipients = [email])
   msg.body = f"This is your reset code {makeResetCode(email).decode('ascii')} if you did not requset this code you can pay this email no mind"
   mail.send(msg)


def makeResetCode(email):
    return User.query.filter_by(email=email).first().token


def getUserFromCode(code):
    user = User.query.filter_by(token=code)
    return user.first()


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    location, fileExtention = os.path.splitext(form_picture.filename)
    fileName = random_hex + fileExtention
    filePath = os.path.join(app.root_path, 'static/images/users/', fileName)

    output_size = (125, 125)
    imageFile = Image.open(form_picture)
    imageFile.thumbnail(output_size)
    imageFile.save(filePath)

    return fileName
