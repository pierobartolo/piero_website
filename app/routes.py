from flask import render_template, session
from datetime import datetime, timedelta
from app.utilities import bioinformatics, covid19
from app.forms import TwoStringsForm
import pandas as pd
from app import app


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
    if datetime.now().hour >= 16 and datetime.now().minute >= 0:
        times = [d.strftime('%-d %b') for d in pd.date_range('24/02/2020', datetime.now().today())]
    else:
        times = [d.strftime('%-d %b') for d in pd.date_range('24/02/2020', datetime.now().today() - timedelta(1))]
    return render_template('covid.html', total=covid_data["total_cases"], new=covid_data["new_cases"], icu=covid_data["icu_cases"], tests=covid_data["tests"], olabels=times)


@app.route("/levenshtein_distance", methods=['POST', 'GET'])
def levenshtein_distance():
    form = TwoStringsForm()
    if form.validate_on_submit():
        session['string1'] = form.string1.data
        session['string2'] = form.string2.data
        session['edit_dist_matrix'] = bioinformatics.calculate_edit_distance(session['string1'], session['string2'])
        return render_template("levenshtein_distance.html", zip=zip, len=len, range=range, form=form)
    else:
        session['string1'] = "ACGG"
        session['string2'] = "ACTC"
        session['edit_dist_matrix'] = bioinformatics.calculate_edit_distance(session['string1'], session['string2'])
        return render_template("levenshtein_distance.html", zip=zip, len=len, range=range, form=form)

@app.route("/real_time_rt")
def real_time_rt():
    original, smoothed = covid19.prepare_cases()
    posteriors = covid19.get_posteriors(smoothed)
    hdis = covid19.highest_density_interval(posteriors)
    most_likely = posteriors.idxmax().rename('ML')
    result = pd.concat([most_likely, hdis], axis=1)
    times = [d.strftime('%-d %b') for d in result.index.get_level_values('data')]
    return render_template("real_time_rt.html",result=result)
