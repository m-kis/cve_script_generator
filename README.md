# cve_script_generator
Ce projet est un générateur de scripts d'exploitation pour les CVE (Common Vulnerabilities and Exposures). 
Il vous permet de rechercher une CVE spécifique dans un dataset CVE fournit, qui sera étoffé avec le temps, d'obtenir des informations sur la CVE et de générer un script d'exploitation à l'aide du modèle de langage Davinci de OpenAI.

# Fonctionnalités
Recherche d'une CVE dans le dataset fournit CVE.
Affichage des informations sur la CVE, y compris le résumé et les instructions d'exploitation.

Génération d'un script d'exploitation en utilisant le modèle de langage Davinci.

Affichage du script d'exploitation généré avec une coloration syntaxique pour une meilleure lisibilité.

Configuration requise
Python 3.x
Flask
pandas
openai
Installation
Clonez le dépôt GitHub sur votre machine locale :
```git clone https://github.com/M-KIS/cve_script_generator.git```

Accédez au répertoire du projet : 
```cd cve-script-generator```
Installez les dépendances requises :
```pip install -r requirements.txt```

#Utilisation 
Assurez-vous d'avoir configuré votre clé API OpenAI. Vous pouvez la définir dans la variable openai.api_key du fichier cve.py.

Placez vos fichiers CSV contenant les données CVE dans le répertoire cve_list.

Lancez l'application en exécutant le script cve.py :
```python cve.py```

Accédez à l'application dans votre navigateur à l'adresse http://localhost:5000.

Recherchez une CVE en saisissant son ID dans le champ de recherche.

Consultez les informations sur la CVE et générez un script d'exploitation en cliquant sur le bouton "Search".

Le script d'exploitation généré sera affiché avec une coloration syntaxique dans un bloc de code.

Si vous souhaitez générer une suite du script, cliquez sur le bouton "Continue Generation" et le script précédent sera inclus dans la requête pour la génération continue. Si la réponse ne convient pas vous pouvez regénrer une autre réponse. 

Contributions
Les contributions à ce projet sont les bienvenues. N'hésitez pas à ouvrir une issue pour signaler des problèmes ou à proposer des améliorations en soumettant une pull request.

Prochaine étape intégrer le modèle pré-entrainer T5 et BERT de M-KIS. 
