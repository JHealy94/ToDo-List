from flask import url_for , Flask , request
from flask import render_template
import os
app = Flask(__name__)

domainName="https://list-himehowareu.c9users.io"

def makeLink(address,name):
    return("<a href='%s'>%s</a>"%(domainName+address,name))

@app.route("/")
def helloW():
    return "Hello World!<br>to say hi to a person go to %s"%(makeLink(url_for("hello"),"hello"))

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    a=request.args.get('a')
    return render_template('hello.html', name=name)
    
@app.route('/list/')
def listurl():
    a=request.args.get('a')
    return str(os.listdir("."))


@app.route('/<file>')
def random(file):
    return render_template(file)
    
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))