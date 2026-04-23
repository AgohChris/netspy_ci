import socket
import subprocess as sb
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.helpers import (afficher_separateur,
                           afficher_titre,
                           obtenir_ip_locale,
                           obtenir_plage_reseau)
from scapy.all import ARP, Ether, srp

try:
    SCAPY_DISPONIBLE = True
except ImportError:
    SCAPY_DISPONIBLE = False


def resoudre_nom(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "N/A"

def lire_table_arp():
    table = {}
    try:
        sortie = sb.check_output("arp -a", shell=True).decode(errors="ignore")
        for ligne in sortie.splitlines():
            parties = ligne.split()
            ip, mac = None, None
            if platform.system() == "Windows":
                if len(parties) >= 2 and parties[0][0].isdigit():
                    ip, mac = parties[0], parties[1]
            else:
                for j, p in enumerate(parties):
                    if p.startswith("(") and p.endswith(")"):
                        ip = p[1:-1]
                    if ":" in p and len(p) == 17:
                        mac = p
            if ip and mac:
                table[ip] = mac
    except Exception:
        pass
    return table


def scan_ping_basique(ip_local):
    print("Scan avec ping en cours sur le réseau local...\n")
    parties = ip_local.split(".")
    base = f"{parties[0]}.{parties[1]}.{parties[2]}"  # fix: espace retiré
    machines = []

    systeme = platform.system()
    # param_ping = "-n 1 -w 500" if systeme == "Windows" else "-c 1 -W 1"

    if systeme == "Windows":
        param_ping = "-n 1 -w 500"
    else:
        param_ping = "-c 1 -W 1"


    def ping_ip(i):
        ip = f"{base}.{i}"
        commande = f"ping {param_ping} {ip}"
        resultat = sb.call(commande, shell=True, stdout=sb.DEVNULL, stderr=sb.DEVNULL)
        if resultat == 0:
            return {"ip": ip, "mac": "N/A", "nom": "N/A"}
        return None

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(ping_ip, i): i for i in range(1, 256)}
        for future in as_completed(futures):
            result = future.result()
            if result:
                machines.append(result)
                print(f"  ✓ Machine active : {result['ip']}")

    table_arp = lire_table_arp()
    for m in machines:
        m["mac"] = table_arp.get(m["ip"], "N/A")
        m["nom"] = resoudre_nom(m["ip"])

    machines.sort(key=lambda m: list(map(int, m["ip"].split("."))))
    return machines


def module_decouverte():
    afficher_titre("MODULE 1 : DÉCOUVERTE RÉSEAU")

    ip_local = obtenir_ip_locale()
    plage = obtenir_plage_reseau(ip_local)

    print(f"\n Votre machine : {ip_local}")
    print(f" Plage d'adresse ip Scannée : {plage}")
    print(f" Méthode utilisée : Scan ARP")

    machines_detectees = []

    if not SCAPY_DISPONIBLE:
        print("\n Attention [!] scapy non installé : scan ARP indisponible")
        machines_detectees = scan_ping_basique(ip_local)
    else:
        print("\n Scan en cours...")
        try:
            paquet_arp = ARP(pdst=plage)
            paquet_ether = Ether(dst="ff:ff:ff:ff:ff")
            paquet = paquet_ether / paquet_arp
            responses, _ = srp(paquet, timeout=3, verbose=False)

            for _, response in responses:
                machines_detectees.append({
                    "ip": response.psrc,
                    "mac": response.hwsrc
                })
        except PermissionError:
            print(" [!] Droits insuffisants — passez en root pour le scan ARP")
            machines_detectees = scan_ping_basique(ip_local)
        except Exception as e:
            print(f" [!] Erreur inattendue : {e}")
            machines_detectees = scan_ping_basique(ip_local)

    afficher_separateur()

    if machines_detectees:
        print(f"  {len(machines_detectees)} machine(s) détectée(s) :\n")
        print(f"  {'N°':<5} {'Adresse IP':<18} {'Adresse MAC':<20} {'Nom d\'hôte'}")
        afficher_separateur()
        for i, machine in enumerate(machines_detectees, 1):
            mac = machine.get("mac", "N/A")
            nom = machine.get("nom", "N/A")
            print(f"  {i:<5} {machine['ip']:<18} {mac:<20} {nom}")
    else:
        print("  Aucune machine détectée.")
        print("  Vérifiez que vous êtes bien connecté au réseau.")


    afficher_separateur()
    input("\n Appuyez sur Entrée pour continuer")

    return machines_detectees