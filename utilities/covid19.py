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
    with open('total_cases.list', 'wb') as data_list:
        pickle.dump(total_cases, data_list)
    with open('icu_cases.list', 'wb') as data_list:
        pickle.dump(icu_cases, data_list)
    with open('tests.list', 'wb') as data_list:
        pickle.dump(tests, data_list)
    with open('new_cases.list', 'wb') as data_list:
        pickle.dump(new_cases, data_list)
