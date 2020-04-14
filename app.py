from flask import Flask, render_template, request, session
from datetime import datetime
from flask_talisman import Talisman
from utilities import bioinformatics, covid19
import pandas as pd
from config import Config


app = Flask(__name__)
talisman = Talisman(app, content_security_policy=Config.csp, content_security_policy_nonce_in=['script-src-elem', 'script-src'])
app.config.from_object(Config)


@app.route("/")
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/covid-19")
def covid():
    covid_data = covid19.update_data()
    times = [d.strftime('%-d %b') for d in pd.date_range('24/02/2020', datetime.now().today())]
    return render_template('covid.html', total=covid_data["total_cases"], new=covid_data["new_cases"], icu=covid_data["icu_cases"], tests=covid_data["tests"], olabels=times)


@app.route("/levenshtein_distance", methods=['POST', 'GET'])
def levenshtein_distance():
    if request.method == 'POST':
        if request.form['string1']:
            session['string1'] = request.form['string1']
        else:
            session['string1'] = ""
        if request.form['string2']:
            session['string2'] = request.form['string2']
        else:
            session['string2'] = ""

        session['edit_dist_matrix'] = bioinformatics.calculate_edit_distance(session['string1'], session['string2'])
        return render_template("levenshtein_distance.html", zip=zip, len=len, range=range)
    else:
        session['string1'] = "dog"
        session['string2'] = "cat"
        session['edit_dist_matrix'] = bioinformatics.calculate_edit_distance(session['string1'], session['string2'])
        return render_template("levenshtein_distance.html", zip=zip, len=len, range=range)


if __name__ == "__main__":
    app.run(threaded=True)





