from flask import Flask, render_template
from second import second
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import pickle
from datetime import datetime

app = Flask(__name__)
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

    times = [d.strftime('%-d %b') for d in pd.date_range('24/02/2020', datetime.now().today())]
    return render_template('covid.html', total=total_cases, icu=icu_cases, olabels=times)


def update_data():
    url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
    regional_data = pd.read_json(url)
    campania_data = regional_data.loc[regional_data["codice_regione"] == 15]
    total_cases = campania_data["totale_casi"].values
    icu_cases = campania_data["terapia_intensiva"].values
    tests = campania_data["tamponi"].values
    with open('total_cases.list', 'wb') as data_list:
        pickle.dump(total_cases, data_list)
    with open('icu_cases.list', 'wb') as data_list:
        pickle.dump(icu_cases, data_list)


sched = BackgroundScheduler(daemon=True)
sched.add_job(update_data, 'cron', hour=11, minute=11)  # TIMEZONE
sched.start()

if __name__ == "__main__":
    app.run(threaded=True)





