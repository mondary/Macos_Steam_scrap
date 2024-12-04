"""
# Journal des modifications

v1 - "La Génèse" - Création du script initial pour récupérer la bibliothèque Steam.
v2 - "Mosaïque Magique" - Ajout de la mise en forme en mosaïque pour afficher les jeux.
v3 - "Recherche Chocolat" - Ajout d'un moteur de recherche et d'un curseur pour régler la taille des tuiles.
v4 - "Design Noir Éblouissant" - Remise du fond en noir et amélioration de l'intégration du champ de recherche et du curseur.
"""

import os
import subprocess
import sys
import webbrowser
import time
import requests
import vdf
import json

# Fichier pour stocker les informations de connexion
CREDENTIALS_FILE = 'credentials.json'

# Fonction pour écrire le journal des modifications dans README.txt
def ecrire_journal_modifications():
    log_entries = [
        "v1 - \"La Génèse\" - Création du script initial pour récupérer la bibliothèque Steam.",
        "v2 - \"Mosaïque Magique\" - Ajout de la mise en forme en mosaïque pour afficher les jeux.",
        "v3 - \"Recherche Chocolat\" - Ajout d'un moteur de recherche et d'un curseur pour régler la taille des tuiles.",
        "v4 - \"Design Noir Éblouissant\" - Remise du fond en noir et amélioration de l'intégration du champ de recherche et du curseur."
    ]
    
    with open('README.txt', 'w', encoding='utf-8') as f:
        f.write("# Journal des modifications\n\n")
        for entry in log_entries:
            f.write(entry + "\n")

# Appeler la fonction pour écrire le journal
ecrire_journal_modifications()

def installer_dependances():
    print("Vérification et installation des dépendances nécessaires...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "vdf"])
        print("Modules 'requests' et 'vdf' installés avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'installation des dépendances : {e}")
        sys.exit(1)

def charger_identifiants():
    """Charge les identifiants depuis le fichier JSON."""
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            return json.load(f)
    return None

def sauvegarder_identifiants(api_key, nom_utilisateur, steam_id):
    """Sauvegarde les identifiants dans un fichier JSON."""
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump({'api_key': api_key, 'nom_utilisateur': nom_utilisateur, 'steam_id': steam_id}, f)

def ouvrir_page_api():
    print("\nOuverture de la page Steam API Key dans votre navigateur...")
    print("Veuillez suivre les instructions sur la page pour obtenir votre clé API.")
    countdown(5)  # Compte à rebours de 5 secondes
    webbrowser.open('https://steamcommunity.com/dev/apikey')  # Ouvrir l'URL après le compte à rebours

def ouvrir_page_steamidfinder(nom_utilisateur):
    print(f"\nOuverture de la page SteamID Finder pour l'utilisateur '{nom_utilisateur}'...")
    print("Veuillez copier votre Steam ID à partir de cette page.")
    countdown(5)  # Compte à rebours de 5 secondes
    webbrowser.open(f'https://www.steamidfinder.com/lookup/{nom_utilisateur}/')  # Ouvrir l'URL après le compte à rebours

def afficher_formulaire():
    print("=" * 50)
    print("  Bienvenue dans le programme de récupération de la bibliothèque Steam")
    print("=" * 50)

def afficher_question(cadre, question):
    print(cadre)
    print(f"  {question}")
    print(cadre)

def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"Attendez {i} secondes...", end='\r')
        time.sleep(1)
    print(" " * 30, end='\r')  # Effacer la ligne

def obtenir_bibliotheque_steam(api_key, steam_id):
    # Appel à l'API Steam pour obtenir la bibliothèque de jeux
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json&include_appinfo=1"
    
    try:
        print("\nRécupération de votre bibliothèque Steam...")
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            jeux = data.get('response', {}).get('games', [])
            
            if jeux:
                print(f"\nNombre total de jeux trouvés : {len(jeux)}")
                # Sauvegarder les jeux dans steam_library.json
                with open('steam_library.json', 'w', encoding='utf-8') as f:
                    json.dump(jeux, f, ensure_ascii=False, indent=4)
                print("Les informations des jeux ont été sauvegardées dans steam_library.json.")
                
                generer_page_web(jeux)
                return jeux  # Retourner la liste des jeux
            else:
                print("Aucun jeu trouvé dans votre bibliothèque.")
        else:
            print(f"Erreur lors de la récupération des données : {response.status_code}")
            print("Vérifiez que votre API Key et votre SteamID sont corrects.")
    
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    
    return []  # Retourner une liste vide si la récupération a échoué

def generer_page_web(jeux, taille_tuile=200):
    """Génère une page HTML affichant les jeux sous forme de mosaïque avec un moteur de recherche."""
    nombre_jeux = len(jeux) if jeux else 0  # Compter le nombre de jeux, afficher 0 si la liste est vide
    nombre_gog = 0  # Remplacez par le nombre de jeux GOG si disponible
    nombre_epic = 0  # Remplacez par le nombre de jeux Epic Games si disponible

    contenu_html = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mes Jeux Steam</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #121212; /* Fond sombre */
            }}
            .header {{
                position: sticky;
                top: 0;
                background-color: #1e1e1e; /* Fond légèrement plus clair */
                padding: 10px;
                text-align: center;
                z-index: 1000;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .header input[type="text"] {{
                width: 40%;
                padding: 10px;
                border: none;
                border-radius: 5px;
                background-color: #000000; /* Fond du champ de recherche noir */
                color: white;
                margin-right: 10px;
            }}
            .header .slider {{
                margin-left: 10px;
                width: 150px; /* Largeur du slider */
            }}
            .header .icon {{
                margin-left: 10px;
                vertical-align: middle;
                width: 20px; /* Largeur de l'icône */
                height: 20px; /* Hauteur de l'icône */
            }}
            .header .game-count {{
                color: white; /* Couleur blanche pour le nombre de jeux */
                margin-left: 5px; /* Espacement entre l'icône et le texte */
            }}
            .container {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                padding: 20px;
                overflow-y: auto;
                height: calc(100vh - 60px); /* Ajuster la hauteur pour le header */
            }}
            .tuile {{
                width: {taille_tuile}px;
                height: {taille_tuile}px;
                margin: 10px;
                background: linear-gradient(135deg, #2c2c2c, #1e1e1e); /* Dégradé */
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                position: relative;
                overflow: hidden;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                border: 2px solid #444; /* Bordure pour plus de définition */
            }}
            .tuile:hover {{
                transform: scale(1.05);
                box-shadow: 0 8px 40px rgba(0, 0, 0, 0.7);
            }}
            .tuile img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                position: absolute;
                top: 0;
                left: 0;
                z-index: 1;
                opacity: 0.8;
                border-radius: 15px; /* Coins arrondis pour l'image */
            }}
            .tuile .overlay {{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5); /* Ombre en bas */
                z-index: 2;
                border-radius: 15px; /* Coins arrondis pour l'overlay */
            }}
            .tuile .text {{
                position: absolute;
                bottom: 10px; /* Positionner le texte en bas */
                left: 10px; /* Positionner le texte à gauche */
                color: white;
                z-index: 3;
                background: rgba(0, 0, 0, 0.7); /* Fond semi-transparent pour le texte */
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8); /* Ombre portée sur le texte */
            }}
            .tuile h2 {{
                font-size: 16px;
                margin: 0;
                font-weight: bold;
                text-align: center; /* Centrer le titre */
            }}
            .tuile .info {{
                font-size: 10px; /* Taille de police réduite pour le temps de jeu */
                margin: 0;
                display: flex;
                justify-content: space-between; /* Aligner les éléments sur la même ligne */
                align-items: center; /* Aligner verticalement */
            }}
            .tuile .info span:last-child {{
                color: #aaa; /* Couleur plus claire pour l'ID */
                font-size: 8px; /* Taille de police encore plus petite pour l'ID */
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <input type="text" placeholder="Rechercher un jeu..." id="searchInput" onkeyup="filterGames()">
            <input type="range" min="100" max="300" value="{taille_tuile}" class="slider" id="tileSizeSlider" onchange="updateTileSize(this.value)">
            <img src="ico_steam.png" alt="Steam" class="icon"> <span class="game-count">{nombre_jeux}</span>
            <img src="ico_gog.png" alt="GOG" class="icon"> <span class="game-count">{nombre_gog}</span>
            <img src="ico_epic.png" alt="Epic Games" class="icon"> <span class="game-count">{nombre_epic}</span>
        </div>
        <div class="container" id="gameContainer">
    """

    for jeu in jeux:
        nom = jeu.get('name', 'Nom inconnu')
        appid = jeu.get('appid', 'ID inconnu')
        temps_jeu = jeu.get('playtime_forever', 0)  # Temps en minutes
        heures = temps_jeu // 60
        minutes = temps_jeu % 60
        image_path = f"steam_images/{appid}.jpg"

        # Afficher le temps de jeu seulement s'il est supérieur à 0
        temps_affiche = f"{heures}h {minutes}min" if temps_jeu > 0 else "0min"

        contenu_html += f"""
            <div class="tuile" data-name="{nom}">
                <img src="{image_path}" alt="{nom}">
                <div class="overlay"></div>
                <div class="text">
                    <h2>{nom}</h2>
                    <div class="info">
                        <span>{temps_affiche}</span>
                        <span>ID: {appid}</span>
                    </div>
                </div>
            </div>
        """

    contenu_html += """
        </div>
        <script>
            function filterGames() {{
                const input = document.getElementById('searchInput');
                const filter = input.value.toLowerCase();
                const container = document.getElementById('gameContainer');
                const tuiles = container.getElementsByClassName('tuile');

                for (let i = 0; i < tuiles.length; i++) {{
                    const nom = tuiles[i].getAttribute('data-name').toLowerCase();
                    if (nom.includes(filter)) {{
                        tuiles[i].style.display = '';
                    }} else {{
                        tuiles[i].style.display = 'none';
                    }}
                }}
            }}

            function updateTileSize(size) {{
                const tuiles = document.getElementsByClassName('tuile');
                for (let i = 0; i < tuiles.length; i++) {{
                    tuiles[i].style.width = size + 'px';
                    tuiles[i].style.height = size + 'px';
                }}
            }}
        </script>
    </body>
    </html>
    """

    with open('mes_jeux.html', 'w', encoding='utf-8') as f:
        f.write(contenu_html)
    
    # Ouvrir le fichier HTML dans le navigateur
    webbrowser.open('mes_jeux.html')

def obtenir_collections(steam_id):
    chemin_base = os.path.expanduser('~/Library/Application Support/Steam/userdata')
    
    for user_folder in os.listdir(chemin_base):
        sharedconfig_path = os.path.join(chemin_base, user_folder, 'config', 'sharedconfig.vdf')
        
        if os.path.exists(sharedconfig_path):
            try:
                with open(sharedconfig_path, 'r', encoding='utf-8') as fichier:
                    config_data = vdf.load(fichier)
                    print(f"\nCollections pour l'utilisateur {user_folder}:")
                    
                    software = config_data.get('UserRoamingConfigStore', {}).get('Software', {})
                    steam = software.get('Valve', {}).get('Steam', {})
                    
                    if 'Apps' in steam:
                        for app_id, app_info in steam['Apps'].items():
                            nom_jeu = app_info.get('name', 'Inconnu')
                            if 'tags' in app_info:
                                print(f"\nJeu {nom_jeu} (ID: {app_id}):")
                                print(f"Collections: {', '.join(app_info['tags'].values())}")
                            else:
                                print(f"\nJeu {nom_jeu} (ID: {app_id}): Pas de collections")
            except Exception as e:
                print(f"Erreur lors de la lecture des collections : {e}")

def obtenir_bibliotheque_et_collections():
    # Ouverture de la page API
    ouvrir_page_api()
    
    # Demande de la clé API
    afficher_question("+" + "-" * 48 + "+", "Entrez votre Steam API Key :")
    api_key = input().strip()
    
    # Demande du nom d'utilisateur Steam
    afficher_question("+" + "-" * 48 + "+", "Saisissez votre pseudo Steam :")
    nom_utilisateur = input().strip()
    
    # Ouverture de la page SteamID Finder
    ouvrir_page_steamidfinder(nom_utilisateur)
    
    # Demande du SteamID
    print("Veuillez copier votre SteamID dans la fenêtre qui vient de s'ouvrir.")
    afficher_question("+" + "-" * 48 + "+", "Entrez votre SteamID64 (le nombre à 17 chiffres) :")
    steam_id = input().strip()
    
    # Obtenir la bibliothèque et sauvegarder les identifiants si réussi
    if obtenir_bibliotheque_steam(api_key, steam_id):
        sauvegarder_identifiants(api_key, nom_utilisateur, steam_id)

def main():
    print("=== Programme de récupération de la bibliothèque Steam ===")
    
    # Charger les identifiants
    identifiants = charger_identifiants()
    
    if identifiants:
        print("Vous avez des identifiants enregistrés.")
        print("1. Lancer la récupération pour '{}'".format(identifiants['nom_utilisateur']))
        print("2. Créer une nouvelle connexion")
        choix = input("Choisissez une option (1 ou 2) : ")
        
        if choix == '1':
            # Utiliser les identifiants stockés
            jeux = obtenir_bibliotheque_steam(identifiants['api_key'], identifiants['steam_id'])
            obtenir_collections(identifiants['steam_id'])
            
            # Demander à l'utilisateur s'il souhaite exécuter steam_images.py
            executer_steam_images = input("Voulez-vous exécuter steam_images.py pour scrapper les images des jeux ? (o/n) : ").strip().lower()
            
            if executer_steam_images == 'o':
                try:
                    subprocess.run([sys.executable, 'steam_images.py'])  # Exécute steam_images.py
                except Exception as e:
                    print(f"Erreur lors de l'exécution de steam_images.py : {str(e)}")
            elif executer_steam_images == 'n':
                print("Exécution annulée.")
            else:
                print("Réponse invalide. Veuillez répondre par 'o' ou 'n'.")
        elif choix == '2':
            obtenir_bibliotheque_et_collections()
        else:
            print("Choix invalide. Veuillez relancer le programme.")
    else:
        print("Aucun identifiant trouvé. Veuillez entrer vos informations.")
        obtenir_bibliotheque_et_collections()

if __name__ == "__main__":
    main()
