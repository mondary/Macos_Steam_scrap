import os
import subprocess
import sys
import webbrowser
import time

def installer_dependances():
    print("Vérification et installation des dépendances nécessaires...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        print("Module 'requests' installé avec succès.")
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

def ouvrir_page_profil():
    print("\nOuverture de votre profil Steam dans votre navigateur...")
    webbrowser.open('https://steamcommunity.com/my/profile')
    print("1. Une fois sur votre profil, copiez l'URL de la page")
    print("2. Si l'URL est du type 'steamcommunity.com/id/votre_nom':")
    print("   - Faites clic droit sur la page")
    print("   - Sélectionnez 'Copier l'URL de la page'")
    print("3. Cherchez le nombre à 17 chiffres dans l'URL (commence par 76561198)")
    time.sleep(3)  # Attendre que l'utilisateur lise les instructions

def obtenir_bibliotheque_steam():
    # Installation des dépendances
    installer_dependances()
    
    # Import de requests après son installation
    import requests
    
    # Ouverture de la page API
    ouvrir_page_api()
    
    # Demande de la clé API
    print("\nEntrez votre Steam API Key (elle ressemble à une longue chaîne de caractères) :")
    api_key = input().strip()
    
    # Ouverture de la page profil
    ouvrir_page_profil()
    
    print("\nEntrez votre SteamID (le nombre à 17 chiffres commençant par 76561198) :")
    steam_id = input().strip()
    
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

if __name__ == "__main__":
    print("=== Programme de récupération de la bibliothèque Steam ===")
    obtenir_bibliotheque_steam()
