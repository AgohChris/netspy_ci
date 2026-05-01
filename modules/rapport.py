import socket
import os
import datetime

from utils.helpers import (
    afficher_titre,
    afficher_separateur,
    obtenir_ip_locale,
    obtenir_plage_reseau
)


# ============================================================
#  Construction du contenu du rapport
# ============================================================

def construire_contenu(machines_trouvees, stats_surveillance, sites_captures=None):

    # On récupère les infos de base sur la machine
    ip_locale = obtenir_ip_locale()
    plage = obtenir_plage_reseau(ip_locale)

    # datetime.now() nous donne la date et l'heure exacte à ce moment
    maintenant = datetime.datetime.now()

    # On va construire le rapport ligne par ligne dans une liste
    # À la fin on assemblera tout avec join()
    lignes = []

    # ── En-tête ──────────────────────────────────────────────
    lignes.append("=" * 60)
    lignes.append("  NETSPY CI — RAPPORT D'AUDIT RÉSEAU")
    lignes.append("  Généré automatiquement par NetSpy CI v1.0")
    lignes.append("=" * 60)

    # strftime() formate la date en texte lisible
    # %d = jour, %m = mois, %Y = année, %H = heure, %M = minute, %S = seconde
    lignes.append("\n  Date et heure    : " + maintenant.strftime("%d/%m/%Y à %H:%M:%S"))
    lignes.append("  Machine auditée  : " + socket.gethostname())
    lignes.append("  IP locale        : " + ip_locale)
    lignes.append("  Plage réseau     : " + plage)

    # ── Section 1 : Machines détectées ───────────────────────
    lignes.append("\n" + "-" * 60)
    lignes.append("  SECTION 1 — MACHINES DÉTECTÉES")
    lignes.append("-" * 60)

    # On vérifie si la liste des machines est vide ou non
    if machines_trouvees:
        lignes.append("\n  Nombre de machines : " + str(len(machines_trouvees)) + "\n")
        lignes.append(f"  {'N°':<5} {'Adresse IP':<20} {'Adresse MAC'}")

        # enumerate() nous donne le numéro et la machine en même temps
        # on commence à 1 pour l'affichage
        for i, machine in enumerate(machines_trouvees, 1):
            mac = machine.get("mac", "N/A")
            lignes.append(f"  {i:<5} {machine['ip']:<20} {mac}")
    else:
        lignes.append("\n  Aucune machine détectée lors de l'audit.")

    # ── Section 2 : Connexion internet ───────────────────────
    lignes.append("\n" + "-" * 60)
    lignes.append("  SECTION 2 — CONNEXION INTERNET")
    lignes.append("-" * 60)

    try:
        ip_google = socket.gethostbyname("google.com")
        lignes.append("\n  Connexion Internet : OPÉRATIONNELLE")
        lignes.append("  DNS Google         : Résolu (" + ip_google + ")")
    except socket.gaierror:
        lignes.append("\n  Connexion Internet : PROBLÈME DÉTECTÉ")

    # ── Section 2B : Sites capturés ──────────────────────────
    lignes.append("\n" + "-" * 60)
    lignes.append("  SECTION 2B — SITES CONSULTÉS SUR LE RÉSEAU")
    lignes.append("-" * 60)

    # sites_captures peut être None si le module 2D n'a pas été lancé
    if sites_captures:
        lignes.append("\n  " + str(len(sites_captures)) + " site(s) détecté(s) durant l'audit :\n")

        for i in range(len(sites_captures)):
            # i+1 pour commencer l'affichage à 1
            lignes.append(f"  {i+1:<4} {sites_captures[i]}")
    else:
        lignes.append("\n  Aucune capture DNS effectuée ou aucun site détecté.")

    # ── Section 3 : Qualité du réseau ────────────────────────
    lignes.append("\n" + "-" * 60)
    lignes.append("  SECTION 3 — QUALITÉ DU RÉSEAU")
    lignes.append("-" * 60)

    # stats_surveillance peut être None si le module 3 n'a pas été lancé
    if stats_surveillance:
        lignes.append("\n  Trafic total mesuré  : " + str(round(stats_surveillance["trafic_total_ko"], 1)) + " Ko")
        lignes.append("  Niveau de trafic     : " + stats_surveillance["qualite"])
        lignes.append("  Stabilité passerelle : " + str(round(stats_surveillance["stabilite_taux"])) + "%")
    else:
        lignes.append("\n  Module surveillance non exécuté.")

    # ── Section 4 : Recommandations ──────────────────────────
    lignes.append("\n" + "-" * 60)
    lignes.append("  SECTION 4 — RECOMMANDATIONS")
    lignes.append("-" * 60)

    # On construit la liste des recommandations selon les résultats
    recommandations = []

    if machines_trouvees and len(machines_trouvees) > 15:
        recommandations.append("  ⚠ Beaucoup de machines détectées. Vérifiez les accès non autorisés.")

    if stats_surveillance and stats_surveillance["stabilite_taux"] < 80:
        recommandations.append("  ⚠ Stabilité insuffisante. Vérifiez la connexion 4G MTN.")

    if stats_surveillance and "ALERTE" in stats_surveillance["qualite"]:
        recommandations.append("  ⚠ Trafic anormal. Investiguer les machines actives.")

    # Si aucune recommandation → tout va bien
    if not recommandations:
        recommandations.append("  ✓ Aucune anomalie majeure. Réseau en bonne santé.")

    # On ajoute chaque recommandation dans les lignes
    for r in recommandations:
        lignes.append(r)

    # ── Pied de page ─────────────────────────────────────────
    lignes.append("\n" + "=" * 60)
    lignes.append("  Fin du rapport — NetSpy CI | NEOPY Formation Réseau N2")
    lignes.append("=" * 60)

    return lignes, maintenant


# ============================================================
#  Fonction principale du module
# ============================================================

def module_rapport(machines_trouvees, stats_surveillance, sites_captures=None):
    afficher_titre("MODULE 4 — RAPPORT D'AUDIT AUTOMATIQUE")
    print("\n  Génération du rapport en cours...")

    # On construit le contenu du rapport
    lignes, maintenant = construire_contenu(
        machines_trouvees,
        stats_surveillance,
        sites_captures
    )

    # On génère un nom de fichier unique avec la date et l'heure
    # Exemple : rapport_netspy_20260423_143022.txt
    nom_fichier = "rapport_netspy_" + maintenant.strftime("%Y%m%d_%H%M%S") + ".txt"

    # On affiche le rapport dans le terminal
    for ligne in lignes:
        print(ligne)

    afficher_separateur()
    print("\n  Sauvegarde du rapport...")

    # On écrit le rapport dans un fichier texte
    # "w" = write (écriture), encoding utf-8 pour les accents et symboles
    try:
        fichier = open(nom_fichier, "w", encoding="utf-8")

        # join() assemble toutes les lignes avec un retour à la ligne entre chaque
        fichier.write("\n".join(lignes))

        fichier.close()

        print("  ✓ Rapport sauvegardé : " + nom_fichier)

        # abspath() donne le chemin complet du fichier sur le disque
        print("  ✓ Emplacement        : " + os.path.abspath(nom_fichier))

    except Exception as e:
        print("  ✗ Erreur lors de la sauvegarde : " + str(e))

    afficher_separateur()
    input("\n  Appuyez sur Entrée pour revenir au menu...")