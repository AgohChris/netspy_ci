import time
import subprocess
import platform
import psutil

from utils.helpers import (
    afficher_titre,
    afficher_separateur,
    obtenir_ip_locale
)

# Durée de la mesure du trafic en secondes
DUREE_MESURE = 10


# ============================================================
#  3A — Mesure du trafic réseau
# ============================================================

def mesurer_trafic():
    print(f"\n [3A] Mesure du trafic réseau ({DUREE_MESURE} secondes)\n")
    print(" Observation en cours...")
    print(f" {'Seconde':<10} {'Données reçues':<20} {'Données envoyées'}")
    afficher_separateur()

    # On prend une première photo des compteurs réseau
    stats_debut = psutil.net_io_counters()

    # On va stocker les mesures de chaque seconde ici
    historique = []

    for seconde in range(1, DUREE_MESURE + 1):

        # On attend 1 seconde
        time.sleep(1)

        # On prend une deuxième photo des compteurs
        stats_fin = psutil.net_io_counters()

        # La différence entre les deux photos = trafic de cette seconde
        # On divise par 1024 pour convertir les octets en kilooctets
        recu_ko = (stats_fin.bytes_recv - stats_debut.bytes_recv) / 1024
        envoye_ko = (stats_fin.bytes_sent - stats_debut.bytes_sent) / 1024

        # On sauvegarde cette mesure dans la liste
        mesure = {
            "seconde": seconde,
            "recu_ko": recu_ko,
            "envoye_ko": envoye_ko
        }
        historique.append(mesure)

        # On affiche la ligne de cette seconde
        print(f" {seconde:<10} {recu_ko:<18.1f} Ko  {envoye_ko:.1f} Ko")

        # La fin devient le début pour la prochaine seconde
        stats_debut = stats_fin

    return historique


# ============================================================
#  3B — Analyse de la qualité du réseau
# ============================================================

def analyser_qualite(historique):
    print("\n [3B] Analyse de la qualité du réseau\n")

    # On calcule les totaux en parcourant la liste historique
    total_recu = 0
    total_envoye = 0

    for mesure in historique:
        total_recu = total_recu + mesure["recu_ko"]
        total_envoye = total_envoye + mesure["envoye_ko"]

    # Moyenne = total divisé par le nombre de secondes
    moyenne_recu = total_recu / len(historique)

    print(f" Total reçu      : {total_recu:.1f} Ko")
    print(f" Total envoyé    : {total_envoye:.1f} Ko")
    print(f" Moyenne/sec     : {moyenne_recu:.1f} Ko/s")

    afficher_separateur()
    print("\n Évaluation de la qualité :\n")

    # On compare la moyenne à des seuils pour déterminer la qualité
    if moyenne_recu < 10:
        qualite = "FAIBLE"
        conseil = "Réseau peu actif ou connexion lente. Vérifiez le signal 4G."
    elif moyenne_recu < 100:
        qualite = "NORMALE"
        conseil = "Trafic normal. Aucune anomalie détectée."
    elif moyenne_recu < 500:
        qualite = "ÉLEVÉE"
        conseil = "Trafic important. Vérifiez s'il y a des téléchargements actifs."
    else:
        qualite = "TRÈS ÉLEVÉE — ALERTE"
        conseil = "Trafic anormal. Possible congestion ou activité suspecte."

    print(f" Niveau de trafic : {qualite}")
    print(f" Conseil          : {conseil}")

    # On retourne un dictionnaire avec les résultats
    resultats = {
        "trafic_total_ko": total_recu + total_envoye,
        "qualite": qualite
    }

    return resultats


# ============================================================
#  3C — Test de stabilité par ping
# ============================================================

def tester_stabilite():
    print("\n [3C] Test de stabilité de la connexion\n")

    # On récupère l'IP locale pour en déduire la passerelle
    ip_locale = obtenir_ip_locale()

    # On découpe l'IP en 4 parties
    # Exemple : "192.168.1.45" → ["192", "168", "1", "45"]
    parties = ip_locale.split(".")

    # La passerelle c'est toujours .1 sur le réseau local
    passerelle = parties[0] + "." + parties[1] + "." + parties[2] + ".1"

    print(f" Passerelle testée : {passerelle}")
    print(f" Nombre de pings   : 5\n")

    # On détecte le système pour adapter la commande ping
    systeme = platform.system()

    reussites = 0

    for i in range(1, 6):

        # La commande ping est différente sur Windows et Linux/Mac
        if systeme == "Windows":
            param = "-n 1 -w 1000"
        else:
            param = "-c 1 -W 1"

        commande = "ping " + param + " " + passerelle

        # On exécute le ping et on récupère le résultat
        # 0 = succès, autre = échec
        resultat = subprocess.call(
            commande,
            shell=True,
            stdout=subprocess.DEVNULL,  # On cache la sortie
            stderr=subprocess.DEVNULL   # On cache les erreurs
        )

        if resultat == 0:
            statut = "✓ Réponse reçue"
            reussites = reussites + 1
        else:
            statut = "✗ Pas de réponse"

        print(f" Ping {i} : {statut}")

    # Calcul du taux de réussite en pourcentage
    taux = (reussites / 5) * 100
    print(f"\n Taux de succès : {taux:.0f}%")

    if taux == 100:
        print(" Stabilité : EXCELLENTE")
    elif taux >= 60:
        print(" Stabilité : ACCEPTABLE — quelques pertes détectées")
    else:
        print(" Stabilité : MAUVAISE — connexion instable")

    return taux


# ============================================================
#  Fonction principale du module
# ============================================================

def module_surveillance():
    afficher_titre("MODULE 3 — SURVEILLANCE & QUALITÉ DU RÉSEAU")

    # Étape 1 : on mesure le trafic et on récupère l'historique
    historique = mesurer_trafic()
    afficher_separateur()

    # Étape 2 : on analyse l'historique pour évaluer la qualité
    stats_qualite = analyser_qualite(historique)
    afficher_separateur()

    # Étape 3 : on teste la stabilité par ping
    taux_stabilite = tester_stabilite()
    afficher_separateur()

    input("\n Appuyez sur Entrée pour continuer...")

    # On retourne tout pour que le rapport puisse l'utiliser
    return {
        "trafic_total_ko": stats_qualite["trafic_total_ko"],
        "qualite": stats_qualite["qualite"],
        "stabilite_taux": taux_stabilite
    }
