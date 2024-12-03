import os
import subprocess
import sys
import webbrowser
import time
import requests
import vdf

def installer_dependances():
    print("Vérification et installation des dépendances nécessaires...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "vdf"])
        print("Modules 'requests' et 'vdf' installés avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'installation des dépendances : {e}")
        sys.exit(1)

def ouvrir_page_api():
    print("\nOuverture de la page Steam API Key dans votre navigateur...")
    webbrowser.open('https://steamcommunity.com/dev/apikey')
    print("1. Connectez-vous à votre compte Steam si ce n'est pas déjà fait")
    print("2. Acceptez les conditions d'utilisation")
    print("3. Entrez un nom de domaine (peut être 'localhost')")
    print("4. Copiez la clé API qui s'affiche")
    time.sleep(3)  # Attendre que l'utilisateur lise les instructions

def ouvrir_page_steamidfinder(nom_utilisateur):
    print(f"\nOuverture de la page SteamID Finder pour l'utilisateur '{nom_utilisateur}'...")
    webbrowser.open(f'https://www.steamidfinder.com/lookup/{nom_utilisateur}/')
    print("Veuillez copier votre Steam ID à partir de cette page.")
    time.sleep(3)  # Attendre que l'utilisateur lise les instructions

def obtenir_bibliotheque_steam(api_key, steam_id):
    # Appel à l'API Steam
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={api_key}&steamid={steam_id}&format=json&include_appinfo=1"
    
    try:
        print("\nRécupération de votre bibliothèque Steam...")
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            jeux = data.get('response', {}).get('games', [])
            
            if jeux:
                print(f"\nNombre total de jeux trouvés : {len(jeux)}")
                print("\nListe de vos jeux Steam :")
                print("-" * 50)
                
                for jeu in jeux:
                    nom = jeu.get('name', 'Nom inconnu')
                    appid = jeu.get('appid', 'ID inconnu')
                    temps_jeu = jeu.get('playtime_forever', 0)  # Temps en minutes
                    
                    # Conversion du temps de jeu en heures et minutes
                    heures = temps_jeu // 60
                    minutes = temps_jeu % 60
                    
                    print(f"Nom: {nom}")
                    print(f"ID: {appid}")
                    print(f"Temps de jeu: {heures}h {minutes}min")
                    print("-" * 50)
            else:
                print("Aucun jeu trouvé dans votre bibliothèque.")
        else:
            print(f"Erreur lors de la récupération des données : {response.status_code}")
            print("Vérifiez que votre API Key et votre SteamID sont corrects.")
    
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

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
    # Installation des dépendances
    installer_dependances()
    
    # Ouverture de la page API
    ouvrir_page_api()
    
    # Demande de la clé API
    print("\nEntrez votre Steam API Key (elle ressemble à une longue chaîne de caractères) :")
    api_key = input().strip()
    
    # Demande du nom d'utilisateur Steam
    print("\nEntrez votre nom d'utilisateur Steam :")
    nom_utilisateur = input().strip()
    
    # Ouverture de la page SteamID Finder
    ouvrir_page_steamidfinder(nom_utilisateur)
    
    # Demande du SteamID
    print("\nEntrez votre SteamID (le nombre à 17 chiffres) :")
    steam_id = input().strip()
    
    # Obtenir la bibliothèque
    obtenir_bibliotheque_steam(api_key, steam_id)
    
    # Obtenir les collections
    obtenir_collections(steam_id)

if __name__ == "__main__":
    print("=== Programme de récupération de la bibliothèque Steam ===")
    obtenir_bibliotheque_et_collections()
