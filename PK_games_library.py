import os
import subprocess
import sys

def afficher_menu():
    print("=== Bienvenue dans votre bibliothèque de jeux ===")
    print("Veuillez choisir un script à exécuter :")
    print("1. Script de récupération de la bibliothèque Steam")
    print("2. Génération du fichier HTML")
    print("3. Script de téléchargement des images des jeux")
    print("4. Quitter")

def executer_script(choix):
    scripts = {
        '1': 'steam/steam_library.py',
        '2': 'steam/steam_htmlgenerator.py',
        '3': 'steam/steam_images.py'
    }
    
    script = scripts.get(choix)
    if script:
        try:
            print(f"Exécution de {script}...")
            subprocess.run([sys.executable, os.path.abspath(script)], check=True)
            print(f"{script} exécuté avec succès.")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution de {script} : {e}")
    else:
        print("Choix invalide. Veuillez réessayer.")

def main():
    while True:
        print("\n" * 3)
        afficher_menu()
        choix = input("Entrez votre choix (1-4) : ")
        
        if choix == '4':
            print("Merci d'avoir utilisé le programme. À bientôt !")
            break
        
        executer_script(choix)

if __name__ == "__main__":
    main()
