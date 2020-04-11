import pickle
import pandas as pd


def update_data():
    url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
    regional_data = pd.read_json(url)
    campania_data = regional_data.loc[regional_data["codice_regione"] == 15]
    total_cases = campania_data["totale_casi"].values
    icu_cases = campania_data["terapia_intensiva"].values
    tests = campania_data["tamponi"].diff().fillna(10).values
    new_cases = campania_data["nuovi_positivi"].values
    covid_data = {"total_cases": total_cases, "icu_cases": icu_cases, "tests": tests, "new_cases": new_cases}

    with open('data/covid_data.dict', 'wb') as data_dict:
        pickle.dump(covid_data, data_dict)

