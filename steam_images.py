import os
import sys
import subprocess

# Fonction pour installer les dépendances
def installer_dependances():
    print("Installation des dépendances nécessaires...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4"])
        print("Les dépendances ont été installées avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'installation des dépendances : {e}")
        sys.exit(1)

# Vérification des dépendances
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Les dépendances nécessaires ne sont pas installées.")
    installer_dependances()  # Installer les dépendances si elles ne sont pas présentes
    # Réessayer d'importer après l'installation
    import requests
    from bs4 import BeautifulSoup

# Fonction pour télécharger l'image du jeu
def telecharger_image_jeu(app_id):
    url = f"https://store.steampowered.com/app/{app_id}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        img_element = soup.select_one('.game_header_image_full')
        
        if img_element and 'src' in img_element.attrs:
            img_url = img_element['src']
            img_response = requests.get(img_url, headers=headers)
            img_response.raise_for_status()
            
            # Sauvegarder l'image
            img_path = os.path.join('steam_images', f'{app_id}.jpg')
            with open(img_path, 'wb') as img_file:
                img_file.write(img_response.content)
            print(f"Image téléchargée pour le jeu {app_id} à l'URL : {img_url}")
            return img_url  # Retourner l'URL de l'image
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image pour le jeu {app_id}: {str(e)}")
    return None

def main(jeux):
    # Créer le dossier steam_images s'il n'existe pas
    if not os.path.exists('steam_images'):
        os.makedirs('steam_images')
        print("Dossier 'steam_images' créé.")

    # Fichier pour stocker les URLs des images
    with open('steam_images/urls.txt', 'w', encoding='utf-8') as url_file:
        # Télécharger les images pour chaque jeu
        for jeu in jeux:
            app_id = jeu['appid']
            img_url = telecharger_image_jeu(app_id)
            if img_url:
                url_file.write(f"{app_id}: {img_url}\n")  # Écrire l'ID et l'URL dans le fichier

if __name__ == "__main__":
    # Exemple de liste de jeux avec leurs IDs
    jeux = [
        {"appid": 570, "name": "Dota 2"},
        {"appid": 730, "name": "Counter-Strike: Global Offensive"},
        {"appid": 440, "name": "Team Fortress 2"},
        # Ajoutez d'autres jeux ici
    ]
    main(jeux)
