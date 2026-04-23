import socket

def afficher_titre(titre):
    print("\n" + "=" * 60)
    print(f"{titre}")
    print("=" * 60)

def afficher_separateur():
    print("-" * 60)

def obtenir_ip_locale():
    try:
       s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       s.connect(("8.8.8.8", 80))
       ip = s.getsockname()[0]
       s.close()
       return ip
    except Exception:
        return "Impossible de detcater l'ip"

def obtenir_plage_reseau(ip_local):
    partie = ip_local.split(".")
    return f"{partie[0]}.{partie[1]}.{partie[2]}"