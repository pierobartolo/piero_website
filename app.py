from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from second import second

app = Flask(__name__)
app.secret_key = "hello"
#app.permanent_session_lifetime = timedelta(days=5)
app.register_blueprint(second, url_prefix="/bioinformatics")


@app.route("/")
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")




if __name__ == "__main__":
    app.run(threaded=True)





