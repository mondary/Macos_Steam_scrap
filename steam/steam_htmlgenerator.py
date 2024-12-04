import os
import json
import webbrowser

# Dossier pour stocker les images
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # Répertoire du script
PARENT_DIR = os.path.dirname(ROOT_DIR)  # Dossier parent
HTML_DIR = os.path.join(PARENT_DIR, 'My_games')  # Dossier pour le fichier HTML
IMAGES_DIR = os.path.join(HTML_DIR, 'steam_images')  # Dossier pour les images dans My_games
# Fichier de la bibliothèque Steam
STEAM_LIBRARY_FILE = os.path.join(ROOT_DIR, 'steam_temp', 'steam_library.json')

# Créer le dossier pour les images s'il n'existe pas
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# Fonction pour trier les jeux
def trier_jeux(jeux, critere):
    if critere == "id":
        return sorted(jeux, key=lambda x: x.get('appid', 0))
    elif critere == "nom":
        return sorted(jeux, key=lambda x: x.get('name', '').lower())
    elif critere == "temps":
        return sorted(jeux, key=lambda x: x.get('playtime_forever', 0))
    return jeux

def generer_page_web(jeux, taille_tuile=300):
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
            .header select {{
                margin-left: 10px;
                padding: 10px;
                border-radius: 5px;
                background-color: #000000; /* Fond du sélecteur noir */
                color: white;
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
                height: {int(taille_tuile * 215 / 460)}px;
                margin: 8px;
                background: linear-gradient(135deg, #2c2c2c, #1e1e1e); /* Dégradé */
                border-radius: 5px;  /* Rayon de 5px */
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                position: relative;
                overflow: hidden;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
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
            }}
            .tuile .text {{
                position: absolute;
                bottom: 0; /* Positionner le texte en bas */
                left: 0; /* Positionner le texte à gauche */
                width: 100%; /* S'étendre sur toute la largeur */
                color: white;
                z-index: 3;
                background: rgba(0, 0, 0, 0.7); /* Fond semi-transparent pour le texte */
                padding: 10px 0; /* Padding en haut et en bas, pas de padding à gauche et à droite */
                border-radius: 0 0 15px 15px; /* Coins arrondis en bas */
                font-size: 14px;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8); /* Ombre portée sur le texte */
                text-align: center; /* Centrer le texte */
                opacity: 0; /* Masquer par défaut */
                transition: opacity 0.3s ease; /* Transition pour l'opacité */
            }}
            .tuile:hover .text {{
                opacity: 1; /* Afficher au survol */
            }}
            .tuile h2 {{
                font-size: 16px;
                margin: 0;
                font-weight: bold;
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
            .badge {{
                padding: 5px 10px;
                border-radius: 5px;
                color: white;
                font-size: 12px;
                display: inline-block;
                margin-right: 5px; /* Espacement entre le badge et l'ID */
                opacity: 0; /* Masquer par défaut */
                transition: opacity 0.3s ease; /* Transition pour l'opacité */
            }}
            .tuile:hover .badge {{
                opacity: 1; /* Afficher au survol */
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <input type="text" placeholder="Rechercher un jeu..." id="searchInput" onkeyup="filterGames()">
            <input type="range" min="100" max="300" value="{taille_tuile}" class="slider" id="tileSizeSlider" onchange="updateTileSize(this.value)">
            <select id="sortSelect" onchange="sortGames()">
                <option value="id">Trier par ID</option>
                <option value="nom">Trier par Nom</option>
                <option value="temps">Trier par Temps de Jeu</option>
            </select>
            <img src="My_games/ico_steam.png" alt="Steam" class="icon"> <span class="game-count">{nombre_jeux}</span>
            <img src="My_games/ico_gog.png" alt="GOG" class="icon"> <span class="game-count">{nombre_gog}</span>
            <img src="My_games/ico_epic.png" alt="Epic Games" class="icon"> <span class="game-count">{nombre_epic}</span>
        </div>
        <div class="container" id="gameContainer">
    """

    for jeu in jeux:
        nom = jeu.get('name', 'Nom inconnu')
        appid = jeu.get('appid', 'ID inconnu')
        temps_jeu = jeu.get('playtime_forever', 0)  # Temps en minutes
        heures = temps_jeu // 60
        minutes = temps_jeu % 60
        image_path = os.path.join(IMAGES_DIR, f"{appid}.jpg")  # Chemin d'image mis à jour

        # Afficher le temps de jeu seulement s'il est supérieur à 0
        temps_affiche = f"{heures}h {minutes}min" if temps_jeu > 0 else "0min"

        # Déterminer la couleur du badge en fonction du temps de jeu
        if temps_jeu < 30:
            badge_couleur = "black"
        elif temps_jeu < 60:
            badge_couleur = "lightcoral"  # Rouge clair
        elif temps_jeu < 180:
            badge_couleur = "lightorange"  # Orange clair
        else:
            badge_couleur = "green"

        # URL de la page Steam du jeu
        url_steam = f"https://store.steampowered.com/app/{appid}/"

        contenu_html += f"""
            <a href="{url_steam}" class="tuile" data-name="{nom}" data-appid="{appid}" data-playtime="{temps_jeu}" target="_blank">
                <img src="{image_path}" alt="{nom}">
                <div class="text">
                    <h2>{nom}</h2>
                    <div class="info">
                        <span class="badge" style="background-color: {badge_couleur};">{temps_affiche}</span>
                        <span>ID: {appid}</span>
                    </div>
                </div>
            </a>
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
                const ratio = 215 / 460;  // Ratio de hauteur à largeur
                for (let i = 0; i < tuiles.length; i++) {{
                    tuiles[i].style.width = size + 'px';
                    tuiles[i].style.height = (size * ratio) + 'px';  // Ajuster la hauteur en fonction du ratio
                }}
            }}

            function sortGames() {{
                const select = document.getElementById('sortSelect');
                const sortBy = select.value;
                const container = document.getElementById('gameContainer');
                const tuiles = Array.from(container.getElementsByClassName('tuile'));

                tuiles.sort((a, b) => {{
                    if (sortBy === 'id') {{
                        return a.getAttribute('data-appid') - b.getAttribute('data-appid');
                    }} else if (sortBy === 'nom') {{
                        return a.getAttribute('data-name').localeCompare(b.getAttribute('data-name'));
                    }} else if (sortBy === 'temps') {{
                        return a.getAttribute('data-playtime') - b.getAttribute('data-playtime');
                    }}
                }});

                // Réorganiser les tuiles dans le conteneur
                tuiles.forEach(tuile => container.appendChild(tuile));
            }}
        </script>
    </body>
    </html>
    """

    # Créer le fichier HTML dans le dossier parent
    with open(os.path.join(PARENT_DIR, 'My_games.html'), 'w', encoding='utf-8') as f:
        f.write(contenu_html)
    
    # Ouvrir le fichier HTML dans le navigateur
    webbrowser.open(os.path.join(PARENT_DIR, 'My_games.html'))

def main():
    """Fonction principale pour générer la page HTML."""
    if os.path.exists(STEAM_LIBRARY_FILE):
        with open(STEAM_LIBRARY_FILE, 'r', encoding='utf-8') as f:
            jeux = json.load(f)
            generer_page_web(jeux)
    else:
        print("Le fichier de bibliothèque Steam n'existe pas.")

if __name__ == "__main__":
    main()
