import socket
from scapy.all import sniff, DNS, DNSQR

from utils.helpers import(
    afficher_titre,
    afficher_separateur,
    obtenir_ip_locale,
    obtenir_plage_reseau
)

PORT_A_TESTER = [
    (22, "SSH"),
    (80, "HTTP"),
    (443, "HTTPS"),
    (21, "FTP"),
    (23, "Telnet"),
    (3306, "MySQL"),
    (445, "Partage Windows"),
    (8291, "Mikrotik"),
]

DOMAINE_A_TESTER = [
    "google.com",
    "facebook.com",
    "neopy.org",
    "youtube.com",
    "jumia.ci",
    "telegram.org",
    "kali.org"
]

def tester_port(machine_detecter):
    print("\n TEST DES PORTS COURANT SUR LES MACHINE DÉETECTÉES \n")

    if not machine_detecter:
        print("Aucune machine à tester. veuillez relancer le module 1 puis réessayer")
    
        return
    
    for machine in machine_detecter:
        ip = machine["ip"]
        print(f"\n Machine : {ip}")

        ports_ouvert = []


        for port, service in PORT_A_TESTER:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                resultat = s.connect_ex((ip, port))
                s.close()

                if resultat == 0:
                    ports_ouvert.append((port, service))
                    print(f"✓Port {port:<6} ({service} : OUVERT)")

            except Exception:
                pass

        if not ports_ouvert:
            print(" Aucun port détecté.")


def tester_dns():
    print("\n test DNS \n")
    print(f"{'Domaine':<25} {'Résultat':<15} {'IP résolue'}")

    afficher_separateur()

    for domaine in DOMAINE_A_TESTER:
        try:
            ip_resolue = socket.gethostbyname(domaine)
            print(f"{domaine:<25} {'✓ OK':<15} {ip_resolue}")
        except socket.gaierror:
            print(f"{domaine:<25} {'échec ✖️':<15} DNS non résolu")
    


def diagnostic_automatique():
    print("\n DIAGNOSTIC AUTOMATIQUE \n")

    # Test internet
    try:
        ip_google = socket.gethostbyname("google.com")
        print(f"✓ Connexion Internet     : Opérationnelle")
        print(f"✓ DNS Google résolu vers : {ip_google}")
    except socket.gaierror:
        print("✗ Connexion Internet     : PROBLÈME DÉTECTÉ")
        print("→ Vérifiez la box MTN / la connexion")

    # Test réseau local
    try:
        ip_locale = obtenir_ip_locale()
        if ip_locale != "Impossible de détecter l'IP":
            print(f"✓ Réseau local           : Actif ({ip_locale})")
        else:
            print("✗ Réseau local           : Non détecté")
    except:
        print("✗ Réseau local           : Erreur")


def monitoring_dns_temps_reel():
    print("\n CAPTURE DNS — SITES CONSULTÉS SUR LE RÉSEAU \n")

    # Vérifier si scapy est disponible
    try:
        scapy_ok = True
    except:
        scapy_ok = False

    if not scapy_ok:
        print("scapy non installé — capture DNS indisponible")
        print("Installez-le avec : pip install scapy")
        input("\nAppuyez sur Entrée pour continuer...")
        return []

    import threading

    duree = 30
    sites_captures = []

    print("Comment ça fonctionne :")
    print("Chaque fois qu'une machine visite un site, elle envoie")
    print("une requête DNS. NetSpy CI intercepte ces requêtes.")
    print("")
    afficher_separateur()
    print(f"Durée de la capture : {duree} secondes")
    print("Lancez des activités sur les machines du réseau...")
    print("")
    afficher_separateur()
    print(f"{'Machine source':<20} {'Site consulté'}")
    afficher_separateur()

    # Fonction appelée pour chaque paquet capturé
    def analyser_paquet(paquet):
        if paquet.haslayer(DNS) and paquet.haslayer(DNSQR):
            try:
                nom_site = paquet[DNSQR].qname.decode().rstrip(".")

                if nom_site not in sites_captures and not nom_site.endswith(".local"):
                    sites_captures.append(nom_site)

                    ip_source = paquet[0].src
                    print(f"  {ip_source:<18} → {nom_site}")
            except:
                pass

    # Fonction qui lance la capture
    def lancer_capture():
        try:
            from scapy.all import sniff, DNS, DNSQR
            sniff(
                filter="udp port 53",
                prn=analyser_paquet,
                timeout=duree,
                store=False,
                promisc=True
            )
        except Exception as e:
            # Si permission refusée, on affiche un message clair
            print("\n  [!] Capture impossible : droits insuffisants.")
            print("  → Relancez avec : sudo python main.py")
        
    # Lancer la capture en parallèle
    thread = threading.Thread(target=lancer_capture)
    thread.start()
    thread.join()

    # Résumé
    afficher_separateur()
    print(f"\n Capture terminée. {len(sites_captures)} site(s) détecté(s) :\n")

    if sites_captures:
        for i in range(len(sites_captures)):
            print(f"  {i+1}. {sites_captures[i]}")
    else:
        print(" Aucun site capturé.")
        print(" → Lancez le script en administrateur (sudo)")
        print(" → Assurez-vous que des machines sont actives")

    afficher_separateur()
    input("\nAppuyez sur Entrée pour continuer...")

    return sites_captures


# ── Fonction principale du module ──────────────────────────

def module_connectivite(machines_detectees):
    afficher_titre("MODULE 2 — TESTS DE CONNECTIVITÉ & MONITORING DNS")

    tester_port(machines_detectees)
    afficher_separateur()

    tester_dns()
    afficher_separateur()

    diagnostic_automatique()
    afficher_separateur()

    sites = monitoring_dns_temps_reel()
    afficher_separateur()

    input("\nAppuyez sur Entrée pour revenir au menu...")

    return sites