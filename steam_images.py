import json
import os
import requests
from bs4 import BeautifulSoup

def extraire_ids_jeux(fichier):
    """Extrait les IDs des jeux depuis steam_library.json."""
    with open(fichier, 'r', encoding='utf-8') as f:
        data = json.load(f)
        ids = []
        
        if isinstance(data, dict) and 'response' in data:
            response = data['response']
            if isinstance(response, dict) and 'games' in response:
                ids = [jeu['appid'] for jeu in response['games']]
            elif isinstance(response, list):
                ids = [jeu['appid'] for jeu in response]  # Si response est une liste
            else:
                print("Le format de 'response' dans steam_library.json n'est pas valide.")
                return []
        elif isinstance(data, list):
            ids = [jeu['appid'] for jeu in data]  # Si le fichier est une liste de jeux
        else:
            print("Le format de steam_library.json n'est pas valide.")
            return []
    
    return ids

def telecharger_image(app_id, url):
    """Télécharge l'image du jeu à partir de l'URL fournie."""
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
            
            # Créer le dossier steam_images s'il n'existe pas
            if not os.path.exists('steam_images'):
                os.makedirs('steam_images')
                print("Dossier 'steam_images' créé.")

            # Sauvegarder l'image
            img_path = os.path.join('steam_images', f'{app_id}.jpg')
            with open(img_path, 'wb') as img_file:
                img_file.write(img_response.content)
            print(f"Image téléchargée pour le jeu {app_id} à l'URL : {img_url}")
        else:
            print(f"Aucune image trouvée pour le jeu {app_id}.")
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image pour le jeu {app_id}: {str(e)}")

def main():
    # Extraire les IDs des jeux depuis steam_library.json
    ids = extraire_ids_jeux('steam_library.json')

    # Créer les URLs pour chaque ID
    urls = {app_id: f"https://store.steampowered.com/app/{app_id}/" for app_id in ids}

    # Télécharger les images pour chaque URL
    for app_id, url in urls.items():
        telecharger_image(app_id, url)

if __name__ == "__main__":
    main()
