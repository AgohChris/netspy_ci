import socket
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
    

