import time

from utils.helpers import afficher_titre, afficher_separateur
from modules.decouverte import module_decouverte


def afficher_menu():
    afficher_titre("NetSpy CI — Outil d'audit réseau | NEOPY 2026")
    print(" Que voulez-vous faire ?  [1]  Module 1 — Découvrir les machines sur le réseau")
    afficher_separateur()
    return input("  Votre choix : ").strip()

def main():
    machines_detectees = []
    stats_reseau = None

    print("\n  Bienvenue dans NetSpy CI.")
    print("  Initialisation en cours...\n")
    time.sleep(1)

    while True:
        choix = afficher_menu()

        if choix == "1":
            machines_detectees = module_decouverte()
        else:
            print("\n  Choix invalide. Entrez 1, 2, 3, 4 ou 0.\n")


if __name__ == "__main__":
    main()