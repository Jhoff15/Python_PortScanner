import socket
from concurrent import futures

# Asynchrone Funktionen brauchen eine Funktion, die den Aufruf managed
# -> hier find_all_async()
def find_all_async(dst_host=str, start_port=int, end_port=int, verbose=False) -> list:
    open_ports=[]

    ## 
    ## Sehr wichtiger HILFSBLOCK. Damit in port_checker keine Exception auftreten, wenn der 
    ## Host nicht existiert, muss hier getestet werden ob eine grundsätzliche Verbindung mit 
    ## dem Host möglich ist.
    ##

    try:
        # sock.connect() versucht eine Verbindung mit der angegebenen IP/Port herzustellen
        hostinfo = socket.gethostbyaddr("127.0.0.2")
        print(f"Hostname: {hostinfo[0]}, Aliaslist: {hostinfo[1]}, Ipaddrlist: {hostinfo[2]}")
        # wird keine Exception ausgelöst geht es hier weiter
        # close() schließt Verbindung und beendet Socket
    #Exception wenn Host nicht erreichbar ist.
    except Exception as e:
        print(f"Der Host existiert nicht. Exception: {e}")
        return []
    ##
    ## Ende HILFSBLOCK
    ##

    # init eines Sockets
    # Mit Socket können zum Beispiel Server-Client kommunikationen realisiert werden
    # Socket kann z.B. mit connect eine TCP-Anfrage an einen Server schicken
    # Bei Servern wird die Funktion socket.listen() aufgerufen, der Socket hört dann einen
    # bestimmten Port ab und wartet auf einkommende Anfragen.
    # https://realpython.com/python-sockets/
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Nach jedem connect oder generellen call wird die timeout Zeit abgewartet, bevor eine 
    # Exception ausgelöst wird.
    sock.settimeout(0.5)

    # Erzeugung der Asynchronen Prozesse https://docs.python.org/3/library/concurrent.futures.html
    with futures.ThreadPoolExecutor(max_workers=2000) as executor:
        # erzeugt eine Liste mit den Typen list[Future[tuple[bool, int]]] , also wird der Wert noch erwartet, da die Werte
        # vom Typ Future sind.
        results = [
            executor.submit(port_checker, dst_host=dst_host, testport=i, verbose=verbose, sock=sock) for i in range(start_port, end_port+1)
        ]
        # Sage dem executor das gewartet werden soll, bis ein Ergebnis zurückkommt
        executor.shutdown(wait=True, cancel_futures=False)
        
        # Wenn thread fertig ist wird der Port der Liste open_ports hinzugefügt
        # muss nicht in genauer Reihenfolge passieren
        for thread in futures.as_completed(results):
            # checken ob der Port offen ist -> Übergebene Bool-Variable
            if thread.result()[0]: open_ports.append(thread.result()[1])
    
    # Liefere Liste zurück
    return open_ports

# Checkt ob ein TCP-Port auf einem Host-System erreichbar/offen ist.
def port_checker(dst_host=str, testport=int, verbose=False, sock=socket) -> tuple[bool, int]:
    # Dieser Print und in line 88 sind zur Verdeutlichung der Asynchronität
    print(f'Port Checker on {testport} started...')

    # um zweite If zu vermeiden wird port_open mit False deklariert und nur bei einem offenen Port überschrieben
    port_open = False

    # Socket für TCP Verbindungen erzeugt. Anmerkung ÄNDERN -------
    # UDP macht keinen Sinn weil es keine Antwort sendet um zu versuchen eine Verbingund einzurichten
    # -> es gibt keine wirklichen offenen UDP Ports
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.settimeout(0.5)

    # connect_ex() agiert genauso wie connect() aus Zeile 27, es wird aber entweder 0 oder 111 zurückgegeben
    # 0: Erfolgreich -> Port offen
    # 111: nicht Erfolgreich -> Port geschlossen oder anderer Fehler
    # wesentlich schneller als connect, da kein try-catch Block benötigt wird.
    val = sock.connect_ex((dst_host, testport))
    # war die Verbindung erfolgreich wird port_open überschrieben
    if val == 0:
        port_open = True
        print(f"Offener Port: {testport}")
    sock.close()

    # ist verbose = true wird diese zusätzliche Zeile ausgegeben.
    if verbose and not port_open: print(f"Geschlossener Port: {testport}")

    print(f'Port Checker on {testport} finished...')
    # gebe ein Bool und den Port zurück
    return port_open, testport
