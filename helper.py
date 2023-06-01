import os
from datetime import datetime

##
## Funktion zur erzeugen des Dictionary der Services-Datei
##
def get_system32_services_dict() -> dict: ## {port: service}
    # Öffne Datei und speichere sie in Variable
    fileread = open("C:\Windows\System32\drivers\etc\services", "r").read()
    # Erstelle eine Liste der einzelnen Zeilen der Services-Datei
    lines_string = fileread.splitlines()

    # erstelle das Dictionary mit {port: service}
    services_dict = {}
    # Laufe durch alle Elemente in lines_string
    for line in lines_string:
        # Splite line beim Hashtag
        split_by_hashtag = line.split(sep="#", maxsplit=2)[0]
        # Splite neue Line in 3 Teile bei Leerzeichen
        split_in_3 = split_by_hashtag.split(maxsplit=3)
        if len(split_in_3) > 1:
            # Trenne zweite Spalte bei "/" auf
            split_port_protc = split_in_3[1].split(sep="/")
            # es wird getestet ob bereits ein Eintrag für den Port existiert
            # siehe port_scanner.py line 61 oder 
            # https://stackoverflow.com/questions/68193407/how-do-i-check-whether-an-open-port-is-tcp-or-udp
            if int(split_port_protc[0]) not in services_dict.keys():
                # trage key, value par in Dictionary ein
                services_dict[int(split_port_protc[0])] = split_in_3[0]
    # gebe Dictionary zurück
    return services_dict

# universelle Funktion zur Eingabe -> Rekursive Funktion
# Eingabe wird in Typ gecastet und erneute Eingabe gefordert
# wenn ein Error auftritt.
def get_input(typ: type, text: str, std_value: any):
    # Input in var speichern 
    var = input(text)

    # checken ob Input leer ist -> Standartwert wird übernommen.
    if not var:
        return std_value
    # Ist der Typ ungleich String wird gecastet und bei falscher Eingabe 
    # eine neue Eingabe gefordert.
    # Wenn typ == String wird Eingabe zurückgegeben
    if typ != str:
        try:
            return typ(var)
        except ValueError:
            print(f"Falsche Eingabe! Geben Sie eine etwas vom Typ {typ} ein.")
            return get_input(typ, text, std_value)
    else:
        return var

# Startpunkt für Eingabe der benötigten Parameter
# Hauptaufgabe = get_input() aufrufen
def get_inputs() -> tuple[str, int, int]:
    dst_host = "127.0.0.1"
    start_port = 0
    end_port = 1025
    
    print("Input startet... (keine Eingabe = Standart Werte)")
    dst_host = get_input(str, f"Gebe die Host-IP ein({dst_host}): ", dst_host)
    start_port = get_input(int, f"Gebe den Start Port ein({start_port}): ", start_port)
    end_port = get_input(int, f"Gebe den End Port ein({end_port}): ", end_port)

    return dst_host, start_port, end_port

# kleine Helper Funktion die den Log-File und das Log-Folder erstellt.
def create_file_name() -> str:
    path = os.path.curdir
    if not os.path.exists(f'{path}/logs'):
        os.mkdir(f'{path}/logs')

    time_now = datetime.now().strftime("%d%m%Y-%H-%M-%S")
    file_name = f"logs\open-ports-{time_now}.log"

    return file_name