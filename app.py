from flask import Flask, render_template
from second import second
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from flask_talisman import Talisman
from utilities import covid19
import pickle
import pandas as pd
from config import Config


app = Flask(__name__)
talisman = Talisman(app, content_security_policy=Config.csp, content_security_policy_nonce_in=['script-src-elem', 'script-src'])
app.config.from_object(Config)
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

    #if datetime.now().hour >= 16 and datetime.now().minute >= 35:
        times = [d.strftime('%-d %b') for d in pd.date_range('24/02/2020', datetime.now().today())]
    #else:
     #   times = [d.strftime('%-d %b') for d in pd.date_range('24/02/2020', datetime.now().today()-timedelta(1))]

    return render_template('covid.html', total=total_cases, new=new_cases, icu=icu_cases, tests=tests, olabels=times)


scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(covid19.update_data, 'cron', hour=16, minute=27)  # Updating COVID Data
scheduler.start()

if __name__ == "__main__":
    app.run(threaded=True)





