# Espagnol

Un carnet personnel pour apprendre l’espagnol depuis le français. Interface responsive, exercices interactifs et base SQLite sur votre ordinateur. Aucun compte, service externe, paquet ou connexion Internet nécessaire après téléchargement.

## Démarrer

Installez **Python 3.10 ou plus récent**, puis téléchargez ce dépôt (bouton GitHub **Code → Download ZIP**, puis décompressez) ou clonez-le :

```sh
git clone https://github.com/Benjpineau/Espagnol.git
cd Espagnol
python server.py
```

Sur macOS / Linux, utilisez `python3 server.py` si nécessaire ; sur Windows, `py server.py` fonctionne également.

Ouvrez **http://localhost:8000** dans votre navigateur. Gardez le terminal ouvert ; `Ctrl+C` arrête le serveur. Si le port est occupé : `python server.py --port 8080` puis ouvrez http://localhost:8080. Le serveur écoute uniquement sur votre ordinateur (127.0.0.1). N’ouvrez pas directement `static/index.html` et ne l’exposez pas sur Internet.

## Environnement virtuel (facultatif)

L’application utilise uniquement la bibliothèque standard de Python : `requirements.txt` ne contient donc aucun paquet externe. Vous pouvez tout de même isoler votre environnement.

Sur macOS / Linux :

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python server.py
```

Sur Windows (PowerShell) :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python server.py
```

Si PowerShell bloque l’activation, utilisez directement `.\.venv\Scripts\python.exe server.py`. Pour quitter un environnement activé : `deactivate`. Le dossier `.venv/` est exclu de Git.

## Trois espaces

- **Vocabulaire** : espagnol → français, français → espagnol ou répartition 50/50, nombre d’entrées au choix, filtre mots / expressions, tirage aléatoire sans répétition, correction et révision des erreurs. Pour un nombre impair, le mode mixte contient une question espagnol → français de plus.
- **Verbes & temps** : tableau de référence par verbe et temps, puis exercice sur les six personnes. Jeu initial de 12 verbes et 5 temps (360 formes) : présent, passé simple, imparfait, futur et conditionnel. Les formes irrégulières des verbes ser, estar, tener et ir sont incluses. Les temps composés, le subjonctif et l’impératif ne sont pas encore inclus.
- **Grammaire** : six fiches consultables et recherchables en français, avec exemples espagnols.

Les réponses ignorent la casse, les espaces superflus et la différence entre apostrophes droites et courbes ; elles vérifient les accents, le ñ, la ponctuation et la traduction exacte du carnet. Des boutons permettent d’insérer les caractères accentués. Les synonymes ne sont pas évalués automatiquement. Le bilan d’exercice reste en mémoire jusqu’à la navigation ou au rechargement.

## Importer votre CSV

Enregistrez votre fichier en **UTF-8**, puis choisissez-le dans « Votre propre carnet ». Taille maximale : 2 Mo. Les virgules, points-virgules et tabulations sont pris en charge. Les en-têtes doivent être exactement ceux ci-dessous (ordre libre) :

```csv
french,espanol,word/expression
le soleil,el sol,word
à demain,hasta mañana,expression
"bonjour, comment ça va ?","hola, ¿qué tal?",expression
```

La troisième colonne contient `word` ou `expression`. Les lignes vides sont ignorées. L’import ajoute les entrées sans remplacer les existantes ; les doublons exacts sont ignorés. Un fichier invalide est rejeté en entier. Exemple téléchargeable dans l’interface ou dans `static/exemple-vocabulaire.csv`.

## Base de données et sauvegarde

Le premier démarrage crée `data/espagnol.sqlite3`, avec 20 entrées de vocabulaire et les conjugaisons initiales. Les imports persistent dans ce fichier. Pour sauvegarder ou transférer votre carnet, arrêtez le serveur et copiez ce fichier. Il est exclu de Git pour garder votre vocabulaire personnel privé.

La table `conjugations` porte une clé primaire composite **(verb, pronoun, tense)**, ainsi que des index secondaires commençant par le temps et par le pronom. Chaque forme est une cellule de la matrice verbe × pronom × temps. Exemple de requête SQLite :

```sql
SELECT form FROM conjugations
WHERE verb = 'tener' AND pronoun = 'yo' AND tense = 'presente';
```

`data.py` contient le jeu initial et les fiches de grammaire. Pour ajouter des verbes, complétez `VERBS` et les exceptions dans `IRREGULAR` (ne traitez pas un verbe irrégulier comme régulier). Les conjugaisons sont amorcées une seule fois : après modification du jeu initial, mettez à jour la base existante avec SQLite ou sauvegardez puis supprimez la base pour réinitialiser tout le carnet. Les fiches de grammaire se mettent à jour au redémarrage.

## Architecture et vérification

- `server.py` : serveur HTTP local, API JSON, import CSV et SQLite ; bibliothèque standard Python uniquement.
- `data.py` : données pédagogiques initiales.
- `static/` : interface HTML, CSS et JavaScript sans dépendances ni ressources distantes.
- `tests/` : tests des conjugaisons, de l’indexation et de l’import.

```sh
python -m unittest discover -s tests -v
node --check static/app.js
```

Le second contrôle est facultatif et nécessite Node.js ; l’application elle-même n’en a pas besoin.
