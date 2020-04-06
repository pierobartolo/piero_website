from flask import Flask, render_template
from second import second
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import pickle
from datetime import datetime, timedelta
from flask_talisman import Talisman

csp = {
    'default-src': [
        '\'self\'',
        '\'unsafe-inline\''
    ],
    'script-src': [
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        'googletagmanager.com',
        'google-analytics.com'
    ],
    'img-src':[ '\'self\' data:',
                'www.googletagmanager.com'],
    'media-src': [
            '*',
        ],
    'script-src-elem': [
        '\'self\'',
        '\'unsafe-inline\'',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net',
        'cdnjs.cloudflare.com',
        'www.googletagmanager.com',

    ],
    'style-src-elem':[
        '\'self\'',
        'use.fontawesome.com'],
    'font-src': '*'

}

app = Flask(__name__)
talisman = Talisman(app, content_security_policy=csp)
app.secret_key = "hardkey"
app.register_blueprint(second, url_prefix="/bioinformatics")


@app.route("/")
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/covid-19")
def covid():
    with open('total_cases.list', 'rb') as data_list:
        total_cases = pickle.load(data_list)
    with open('icu_cases.list', 'rb') as data_list:
        icu_cases = pickle.load(data_list)
    with open('tests.list', 'rb') as data_list:
        tests = pickle.load(data_list)
    with open('new_cases.list', 'rb') as data_list:
        new_cases = pickle.load(data_list)

    if datetime.now().hour >= 16 and datetime.now().minute >= 35:
        times = [d.strftime('%-d %b') for d in pd.date_range('24/02/2020', datetime.now().today())]
    else:
        times = [d.strftime('%-d %b') for d in pd.date_range('24/02/2020', datetime.now().today()-timedelta(1))]

    return render_template('covid.html', total=total_cases, new=new_cases, icu=icu_cases, tests=tests, olabels=times)


def update_data():
    url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
    regional_data = pd.read_json(url)
    campania_data = regional_data.loc[regional_data["codice_regione"] == 15]
    total_cases = campania_data["totale_casi"].values
    icu_cases = campania_data["terapia_intensiva"].values
    tests = campania_data["tamponi"].diff().fillna(10).values
    new_cases = campania_data["nuovi_positivi"].values
    with open('total_cases.list', 'wb') as data_list:
        pickle.dump(total_cases, data_list)
    with open('icu_cases.list', 'wb') as data_list:
        pickle.dump(icu_cases, data_list)
    with open('tests.list', 'wb') as data_list:
        pickle.dump(tests, data_list)
    with open('new_cases.list', 'wb') as data_list:
        pickle.dump(new_cases, data_list)


sched = BackgroundScheduler(daemon=True)
sched.add_job(update_data, 'cron', hour=16, minute=35)  # TIMEZONE

sched.start()

if __name__ == "__main__":
    app.run(threaded=True)





