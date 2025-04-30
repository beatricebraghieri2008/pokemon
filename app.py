from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

# Carica il dataframe di Pokémon
dataframe_pokemon = pd.read_csv('pokemon (1).csv')

# Imposta i punti totali iniziali
punti_totali = 100

# Probabilità per ogni rarità
probabilità = {
    'Comune': 0.7,
    'Non Comune': 0.2,
    'Rara': 0.09,
    'Ultra Rara': 0.01
}

# Route per la home
@app.route('/')
def home():
    return render_template('index.html')

# Route per aprire il pacchetto
@app.route('/apri_pacchetto')
def apri_pacchetto():
    pacchetto = []
    punti_guadagnati = 0
    
    # Controlla se l'utente ha abbastanza punti per aprire il pacchetto
    if punti_totali >= 10:
        punti_totali -= 10  # Deduci 10 punti dal totale per aprire il pacchetto

        # Seleziona 5 carte in base alla probabilità
        for rarita_casuale in ['Comune', 'Non Comune', 'Rara', 'Ultra Rara']:
            # Filtra le carte per la rarità
            carte_rarita = dataframe_pokemon[dataframe_pokemon['Rarità'] == rarita_casuale]
            
            if len(carte_rarita) > 0:
                carta = carte_rarita.iloc[0]  # Seleziona la prima carta disponibile con quella rarità
                pacchetto.append(carta.to_dict())

                # Aggiorna i punti guadagnati in base alla rarità
                if rarita_casuale == 'Comune':
                    punti_guadagnati += 2
                elif rarita_casuale == 'Non Comune':
                    punti_guadagnati += 5
                elif rarita_casuale == 'Rara':
                    punti_guadagnati += 10
                elif rarita_casuale == 'Ultra Rara':
                    punti_guadagnati += 20

        # Aggiungi i punti guadagnati ai punti totali
        punti_totali += punti_guadagnati

        # Salva la collezione di carte
        salva_collezione(pacchetto)

        # Renderizza la pagina con i dettagli
        return render_template('index.html', output=f"Hai guadagnato {punti_guadagnati} punti.", pacchetto=pacchetto)
    else:
        return render_template('index.html', output="Non hai abbastanza punti per aprire il pacchetto.")

# Funzione per salvare la collezione di carte
def salva_collezione(pacchetto):
    try:
        # Carica la collezione esistente dal file CSV
        collezione = pd.read_csv('carte_trovate.csv')  
    except:
        # Se il file non esiste, crea un DataFrame vuoto
        collezione = pd.DataFrame()

    # Aggiungi i nuovi dati alla collezione
    collezione = collezione.append(pd.DataFrame(pacchetto), ignore_index=True)

    # Salva la collezione aggiornata nel file CSV
    collezione.to_csv('carte_trovate.csv', index=False)

# Route per mostrare la collezione di carte
@app.route('/mostra_collezione')
def mostra_intera_collezione():
    try:
        # Carica la collezione dal file CSV
        collezione_completa = pd.read_csv('carte_trovate.csv')
    except:
        collezione_completa = pd.DataFrame()

    if len(collezione_completa) == 0:
        return render_template('index.html', output="Nessuna collezione trovata.")
    
    # Mostra la collezione
    collezione_completa = collezione_completa.to_dict(orient='records')
    return render_template('index.html', output="Ecco la tua collezione:", pacchetto=collezione_completa)

# Route per mostrare i punti totali
@app.route('/mostra_punti')
def mostra_punti():
    return render_template('index.html', output=f"Hai {punti_totali} punti.")

# Avvia l'applicazione
if __name__ == '__main__':
    app.run(debug=True)
