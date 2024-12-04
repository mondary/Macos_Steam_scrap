import json

def extraire_ids_jeux(fichier):
    """Extrait les IDs des jeux depuis steam_library.json."""
    with open(fichier, 'r', encoding='utf-8') as f:
        data = json.load(f)
        ids = []
        
        # Vérifiez si 'response' est un dictionnaire ou une liste
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

def main():
    # Extraire les IDs des jeux depuis steam_library.json
    ids = extraire_ids_jeux('steam_library.json')

    # Créer les URLs pour chaque ID
    urls = {app_id: f"https://store.steampowered.com/app/{app_id}/" for app_id in ids}

    # Sauvegarder les URLs dans steam_images.json
    with open('steam_images.json', 'w', encoding='utf-8') as url_file:
        json.dump(urls, url_file, ensure_ascii=False, indent=4)
    print("Les URLs des jeux ont été sauvegardées dans steam_images.json.")

if __name__ == "__main__":
    main()
