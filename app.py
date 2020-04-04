from flask import Flask, render_template,session
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

    legend = 'Total Cases'
    temperatures = total_cases
    times = [d.strftime('%d-%m-%Y') for d in pd.date_range('24/02/2020',datetime.now().today())]
    return render_template('covid.html', values=temperatures, labels=times, legend=legend)


def update_data():
    url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
    regional_data = pd.read_json(url)
    campania_data = regional_data.loc[regional_data["codice_regione"] == 15]
    total_cases = campania_data["totale_casi"].values
    with open('total_cases.list', 'wb') as data_list:
        pickle.dump(total_cases, data_list)


sched = BackgroundScheduler(daemon=True)
sched.add_job(update_data, 'interval', minutes=60)
sched.start()

if __name__ == "__main__":
    app.run(threaded=True, debug=True, port=4999)





