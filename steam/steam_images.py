import os
import json
import requests
import logging
import sys

# Configuration de la journalisation
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'steam_temp')  # Dossier pour le log
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)  # Créer le dossier s'il n'existe pas

logging.basicConfig(filename=os.path.join(LOG_DIR, 'steam_images.log'), level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Dossier pour stocker les images
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # Répertoire du script
PARENT_DIR = os.path.dirname(ROOT_DIR)  # Dossier parent
IMAGES_DIR = os.path.join(PARENT_DIR, 'My_games', 'steam_images')  # Dossier pour les images

# Créer le dossier pour les images s'il n'existe pas
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

def extraire_ids_jeux(fichier):
    """Extrait les IDs des jeux depuis steam_library.json et retourne le nombre total d'IDs."""
    chemin_fichier = os.path.join(ROOT_DIR, 'steam_temp', fichier)
    with open(chemin_fichier, 'r', encoding='utf-8') as f:
        data = json.load(f)
        ids = []
        if isinstance(data, dict) and 'response' in data:
            response = data['response']
            if isinstance(response, dict) and 'games' in response:
                ids = [jeu['appid'] for jeu in response['games']]
            elif isinstance(response, list):
                ids = [jeu['appid'] for jeu in response]  # Si response est une liste
            else:
                logging.warning("Le format de 'response' dans steam_library.json n'est pas valide.")
                return [], 0
        elif isinstance(data, list):
            ids = [jeu['appid'] for jeu in data]  # Si le fichier est une liste de jeux
        else:
            logging.warning("Le format de steam_library.json n'est pas valide.")
            return [], 0
    
    return ids, len(ids)  # Retourner les IDs et le nombre total

def afficher_barre_progression(progress, total, description=""):
    """Affiche une barre de progression dans le terminal."""
    percent = (progress / total) * 100
    bar_length = 40  # Longueur de la barre
    block = int(bar_length * progress // total)
    bar = '#' * block + '-' * (bar_length - block)
    sys.stdout.write(f'\r[{bar}] {percent:.2f}% {description}')
    sys.stdout.flush()

def telecharger_image(app_id, url):
    """Télécharge l'image du jeu à partir de l'URL fournie."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        logging.info(f"Tentative de téléchargement de l'image pour le jeu ID: {app_id}")
        response = requests.get(url, headers=headers, allow_redirects=True, stream=True)
        response.raise_for_status()
        
        # Vérifiez si l'URL finale est celle du jeu
        if "agecheck" in response.url:
            logging.warning(f"Redirection vers une page d'âge pour le jeu ID: {app_id}.")
            return
        
        img_path = os.path.join(IMAGES_DIR, f'{app_id}.jpg')  # Chemin d'image mis à jour
        
        # Utiliser la barre de progression pour le téléchargement de l'image
        total_size = int(response.headers.get('content-length', 0))  # Taille totale du fichier
        with open(img_path, 'wb') as img_file:
            for data in response.iter_content(chunk_size=1024):
                img_file.write(data)
                afficher_barre_progression(img_file.tell(), total_size)  # Mettre à jour la barre de progression de l'image
        
        print()  # Nouvelle ligne après la barre de progression
        logging.info(f"Image téléchargée pour le jeu {app_id} à l'URL : {url}")
    except Exception as e:
        logging.error(f"Erreur lors du téléchargement de l'image pour le jeu {app_id}: {str(e)}")

def main():
    """Fonction principale pour télécharger les images."""
    ids, total_images = extraire_ids_jeux('steam_library.json')  # Obtenir les IDs et le nombre total
    if total_images == 0:
        print("Aucune image à télécharger.")
        return

    for index, app_id in enumerate(ids):
        url = f"https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/{app_id}/capsule_616x353.jpg"
        telecharger_image(app_id, url)
        afficher_barre_progression(index + 1, total_images, "Téléchargement des images")  # Mettre à jour la barre de progression globale

    print()  # Nouvelle ligne après la barre de progression globale

if __name__ == "__main__":
    main()
