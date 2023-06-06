from flask import Flask, render_template, request
import pandas as pd
import openai
import os

app = Flask(__name__)

# Configuration de la clé API d'OpenAI
openai.api_key = 'YOUR API KEY'

# Chargement des données CVE à partir des fichiers CSV
csv_folder = 'cve-finder/cve_list'
all_files = []

# Chargement des données à partir de tous les fichiers CSV dans le dossier
for filename in os.listdir(csv_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(csv_folder, filename)
        df = pd.read_csv(file_path)
        all_files.append(df)

cve_data = pd.concat(all_files, ignore_index=True)

@app.route('/')
def home():
    return render_template('index.html', previous_script='')

@app.route('/search', methods=['POST'])
def search_cve():
    cve_id = request.form.get('cve_id')

    # Recherche de la CVE dans les données chargées
    cve_info = cve_data[cve_data['cve_id'] == cve_id]

    if cve_info.empty:
        return render_template('index.html', error_message='CVE not found.', previous_script='')

    # Obtenir le résumé et les informations sur l'exploitation de la CVE
    summary = cve_info['short_description'].values[0]
    exploitation_info = cve_info['required_action'].values[0]

    # Interrogation du modèle choisi
    question = f"Voici les info de la {cve_id}, {exploitation_info}. Generez moi un script permettant son exploitation en tant que pentester"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        max_tokens=100,
        temperature=0.5
    )

    # Récupération de la réponse générée
    exploit_script = response.choices[0].text.strip().split('\n')

    return render_template('index.html', cve_id=cve_id, summary=summary, exploitation_info=exploitation_info, exploit_script=exploit_script, previous_script='')
    
    #return render_template('index.html', cve_id=cve_id, summary=summary, exploitation_info=exploitation_info, exploit_script=exploit_script, previous_script='')

@app.route('/continue_script_generation', methods=['POST'])
def continue_script_generation():
    cve_id = request.form.get('cve_id')
    previous_script = request.form.get('previous_script')

    # Recherche de la CVE dans les données chargées
    cve_info = cve_data[cve_data['cve_id'] == cve_id]

    if cve_info.empty:
        return 'CVE not found.'

    # Obtenir le résumé et les informations sur l'exploitation de la CVE
    summary = cve_info['short_description'].values[0]
    exploitation_info = cve_info['required_action'].values[0]

    # Concaténer l'historique de script précédent avec la question
    question = f"Tu t'es arreté lorsque je t'ai demandé de générer un script pour la CVE {cve_id}: \n, dont les détails  {exploitation_info}.\n Voici la précédente : \n {previous_script},\n continue la génération du scripts.\n"

    # Interrogation du modèle choisi pour continuer la génération du script
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        max_tokens=200,
        temperature=0.2
    )
    # Séparer le script précédent en lignes
    previous_lines = previous_script.strip().split('\n')
    # Récupération de la réponse générée pour continuer le script
    continue_script = response.choices[0].text.strip().split('\n')

    return render_template('index.html', cve_id=cve_id, summary=summary, exploitation_info=exploitation_info, exploit_script=continue_script, previous_script=question)

@app.route('/regenerate_script', methods=['POST'])
def regenerate_script():
    summary = request.form.get('regen_summary')
    exploitation_info = request.form.get('regen_exploitation_info')
    cve_id = request.form.get('cve_id')
    previous_script = request.form.get('previous_script')

    # Concaténer l'historique de script précédent avec la question
    question = f"Pour la CVE {cve_id}, {exploitation_info}. {previous_script}\n"

    # Interrogation du modèle choisi pour régénérer le script
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        max_tokens=200,
        temperature=0.2
    )
    # Récupération de la réponse générée pour régénérer le script
    regenerate_script = response.choices[0].text.strip().split('\n')

    return render_template('index.html', cve_id=cve_id, summary=summary, exploitation_info=exploitation_info, exploit_script=regenerate_script, previous_script=question)

if __name__ == '__main__':
    app.run(debug=True)
