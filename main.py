import time

from utils.helpers import afficher_titre, afficher_separateur
from modules.decouverte import module_decouverte
# from modules.connectivite import module_connectivite
# from modules.surveillance import module_surveillance
# from modules.rapport import module_rapport


def afficher_menu():
    afficher_titre("NetSpy CI — Outil d'audit réseau | NEOPY 2026")
    print("""
  Que voulez-vous faire ?

  [1]  Module 1 — Découvrir les machines sur le réseau
#   [2]  Module 2 — Tester la connectivité et le DNS
#   [3]  Module 3 — Surveiller la qualité du réseau
#   [4]  Module 4 — Générer le rapport d'audit complet
  [0]  Quitter NetSpy CI
    """)
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
        # elif choix == "2":
        #     module_connectivite(machines_detectees)
        # elif choix == "3":
        #     stats_reseau = module_surveillance()
        # elif choix == "4":
        #     module_rapport(machines_detectees, stats_reseau)
        # elif choix == "0":
        #     print("\n  Fermeture de NetSpy CI. À bientôt.\n")
        #     break
        else:
            print("\n  Choix invalide. Entrez 1, 2, 3, 4 ou 0.\n")


if __name__ == "__main__":
    main()