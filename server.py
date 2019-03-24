from flask import render_template, Flask, flash
from flask import redirect, url_for
from forms import SignupForm, LoginForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "shhh_dont_tell_anyone"

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/login", methods=["get", "post"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login.html", title="Login", form=form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["get", "post"])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        flash(f'account made for {form.name.data}For {form.email.data}', "success")
        redirect(url_for("index"))
    return render_template("register.html", title="Register", form=form)

app.run()