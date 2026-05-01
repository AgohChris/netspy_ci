import time

from utils.helpers import afficher_titre, afficher_separateur
from modules.decouverte import module_decouverte
from modules.connectivite import module_connectivite
from modules.surveillance import module_surveillance
from modules.rapport import module_rapport


def afficher_menu():
    afficher_titre("NetSpy CI — Outil d'audit réseau | NEOPY 2026")
    print("  Que voulez-vous faire ?\n")
    print("  [1]  Module 1 — Découvrir les machines sur le réseau")
    print("  [2]  Module 2 — Tester la connectivité et le DNS")
    print("  [3]  Module 3 — Surveiller la qualité du réseau")
    print("  [4]  Module 4 — Générer le rapport d'audit complet")
    print("  [0]  Quitter NetSpy CI")
    print("")
    afficher_separateur()
    return input("  Votre choix : ").strip()


def main():
    # Ces variables gardent les données entre les modules
    # Si on lance le module 4 sans avoir lancé le 1, ça ne plante pas
    machines_detectees = []
    sites_captures = []
    stats_reseau = None

    print("\n  Bienvenue dans NetSpy CI.")
    print("  Initialisation en cours...\n")
    time.sleep(1)

    while True:
        choix = afficher_menu()

        if choix == "1":
            # On stocke les machines trouvées pour les passer aux autres modules
            machines_detectees = module_decouverte()
 
        elif choix == "2":
            # On passe les machines détectées pour tester leurs ports
            # On récupère les sites capturés pour le rapport
            sites_captures = module_connectivite(machines_detectees)

        elif choix == "3":
            # On récupère les stats réseau pour le rapport
            stats_reseau = module_surveillance()

        elif choix == "4":
            # On passe tout ce qu'on a collecté pour générer le rapport complet
            module_rapport(machines_detectees, stats_reseau, sites_captures)

        elif choix == "0":
            print("\n  Fermeture de NetSpy CI. À bientôt.\n")
            break

        else:
            print("\n  Choix invalide. Entrez 1, 2, 3, 4 ou 0.\n")


if __name__ == "__main__":
    main()