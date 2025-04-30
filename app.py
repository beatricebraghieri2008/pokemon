from flask import Flask, render_template, request, redirect, url_for
import random
import pandas as pd
import csv

app = Flask(__name__)

dataframe_pokemon = pd.read_csv('pokemon (1).csv')
punti_totali = 100
probabilità = {
    'Comune': 0.7,
    'Non Comune': 0.2,
    'Rara': 0.09,
    'Ultra Rara': 0.01
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/apri_pacchetto')
def apri_pacchetto():
    global punti_totali
    pacchetto = []
    punti_guadagnati = 0
    if punti_totali >= 10:
        punti_totali -= 10
        for _ in range(5):
            rarita_casuale = random.choices(list(probabilità.keys()), weights=probabilità.values(), k=1)[0]
            carta = dataframe_pokemon[dataframe_pokemon['Rarità'] == rarita_casuale].iloc[0].to_dict()
            pacchetto.append(carta)

            if rarita_casuale == 'Comune':
                punti_guadagnati += 2
            elif rarita_casuale == 'Non Comune':
                punti_guadagnati += 5
            elif rarita_casuale == 'Rara':
                punti_guadagnati += 10
            elif rarita_casuale == 'Ultra Rara':
                punti_guadagnati += 20

        punti_totali += punti_guadagnati
        salva_collezione(pacchetto)
        return render_template('index.html', output=f"Hai guadagnato {punti_guadagnati} punti.", pacchetto=pacchetto)
    else:
        return render_template('index.html', output="Non hai abbastanza punti.")

@app.route('/mostra_collezione')
def mostra_intera_collezione():
    try:
        collezione_completa = pd.read_csv('carte_trovate.csv').to_dict(orient='records')
        return render_template('index.html', output="Ecco la tua collezione:", pacchetto=collezione_completa)
    except FileNotFoundError:
        return render_template('index.html', output="Nessuna collezione trovata.")

@app.route('/mostra_punti')
def mostra_punti():
    return render_template('index.html', output=f"Hai {punti_totali} punti.")

def salva_collezione(pacchetto):
    try:
        collezione = pd.read_csv('carte_trovate.csv')
        collezione = pd.concat([collezione, pd.DataFrame(pacchetto)], ignore_index=True)
    except FileNotFoundError:
        collezione = pd.DataFrame(pacchetto)
    collezione.to_csv('carte_trovate.csv', index=False)

if __name__ == '__main__':
    app.run(debug=True)