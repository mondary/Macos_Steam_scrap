import os
import vdf

def demander_plateforme():
    while True:
        print("\nChoisissez votre plateforme :")
        print("1. MacOS")
        print("2. Windows")
        print("3. Linux")
        choix = input("Entrez le numéro correspondant (1, 2 ou 3) : ").strip()
        
        if choix in ['1', '2', '3']:
            return choix
        print("Choix invalide. Veuillez entrer 1, 2 ou 3.")

def lire_bibliotheque_steam(plateforme):
    # Définir le chemin de base selon la plateforme
    if plateforme == '1':  # MacOS
        chemin_base = os.path.expanduser('~/Library/Application Support/Steam')
    elif plateforme == '2':  # Windows
        chemin_base = 'C:\\Program Files (x86)\\Steam'
    else:  # Linux
        chemin_base = os.path.expanduser('~/.steam/steam')
    
    print(f"Recherche dans : {chemin_base}")
    
    # Chemin vers le fichier libraryfolders.vdf principal
    chemin_library = os.path.join(chemin_base, 'steamapps', 'libraryfolders.vdf')
    print(f"Vérification du fichier : {chemin_library}")
    
    bibliotheques = []
    
    # Lecture du fichier libraryfolders.vdf
    if os.path.exists(chemin_library):
        try:
            with open(chemin_library, 'r', encoding='utf-8') as f:
                data = vdf.load(f)
                print("\nContenu du fichier libraryfolders.vdf:")
                print(data)
                
                # Ajouter le dossier Steam principal
                bibliotheques.append(os.path.join(chemin_base, 'steamapps'))
                
                # Ajouter les autres bibliothèques
                for folder_id, folder_info in data.get('libraryfolders', {}).items():
                    if isinstance(folder_info, dict) and 'path' in folder_info:
                        path = folder_info['path']
                        steamapps_path = os.path.join(path, 'steamapps')
                        bibliotheques.append(steamapps_path)
        except Exception as e:
            print(f"Erreur lors de la lecture de libraryfolders.vdf : {e}")
    
    # Parcourir toutes les bibliothèques trouvées
    for bibliotheque in bibliotheques:
        print(f"\nRecherche des jeux dans : {bibliotheque}")
        if os.path.exists(bibliotheque):
            for fichier in os.listdir(bibliotheque):
                if fichier.startswith('appmanifest_') and fichier.endswith('.acf'):
                    chemin_manifest = os.path.join(bibliotheque, fichier)
                    try:
                        with open(chemin_manifest, 'r', encoding='utf-8') as f:
                            manifest_data = vdf.load(f)
                            app_state = manifest_data.get('AppState', {})
                            nom_jeu = app_state.get('name', 'Inconnu')
                            app_id = app_state.get('appid', 'Inconnu')
                            print(f"Jeu trouvé : {nom_jeu} (ID: {app_id})")
                    except Exception as e:
                        print(f"Erreur lors de la lecture du manifeste {fichier}: {e}")

if __name__ == "__main__":
    plateforme = demander_plateforme()
    lire_bibliotheque_steam(plateforme)
