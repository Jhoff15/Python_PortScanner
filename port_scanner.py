import socket

##später löschen, nur für test -> line 55 lesen
print("Hello World")
## 

## find_open_ports Funktion wie in Screenshot in Aufgabe
## kleine Änderungen weils schöner ist
## line 15: -> list, gibt return Datentyp an. Return ist jetzt bei Aufruf sichtbar, 
## line 15: verbose = 0, gibt default Value an, wenn kein Parameter übergeben wird. Ansonsten evtl error wenn aus anderem Script aufgerufen.
## line 43: sock.shutdown(socket.SHUT_RD), schließt Verbindung mit Socket und sendet FIN / EOF
## line 46: Exception wird jetzt mit Print ausgegben, evtl. hilfreich für Analyse
## line 49+: finally Block wird immer ausgeführt
## sock.close(), deallociert socket, dekrementiert handle count (laufen noch andere Prozesse die IP/Port connected sind kein FIN/EOF)
## https://stackoverflow.com/questions/409783/socket-shutdown-vs-socket-close
def find_open_ports(dst_host, start_port, end_port, verbose=0) -> list:
    # initialisiere leere Liste für Ports
    open_ports = []

    # Standart Python for-loop, range(A, B) erzeugt Array A + alle Werte zwischen A und B
    # Beispiel: A = 2, B = 6, range(A, B) = [2, 3, 4, 5]
    for testport in range(start_port, end_port):
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

        # try-catch Block mit dem auf Fehlermeldungen(Exceptions) im Code reagiert werden kann
        # Expections werden ggf. in Variable e gespeichert
        try:
            # sock.connect() stellt versucht eine Verbindung mit der angegebenen IP/Port herzustellen
            sock.connect((dst_host, int(testport)))
            # wird keine Exception ausgelöst geht es hier weiter
            # <list>.append() hängt ein beliebiges Element an eine Liste an
            open_ports.append(testport)
            print(f"Offener Port: {testport}")
            # sock.shutdown(socket.SHUT_RD), schließt Verbindung mit Socket und sendet FIN / EOF
            sock.shutdown(socket.SHUT_RD)

        except Exception as e:
            if verbose == 1: print(f"Geschlossener Port: {testport} Expection: {e}")
        
        # finally Block wird immer aufgerufen egal ob try eine Exception wirft oder nicht
        finally:
            # sock.close(), deallociert socket, dekrementiert handle count (laufen noch andere Prozesse die IP/Port connected sind kein FIN/EOF)
            sock.close()
    
    return open_ports

## Dieser Block ist Best-Practice für Python Programme.
## Wenn portscanner als Script ausgeführt wird, wird dieser Block ausgeführt.
## Wenn portscanner als Modul in einem zweiten Script aufgerufen wird, wird nichts automatisch ausgeführt.
## -> kein Code wird ausgeführt, wenns nicht gewollt ist
##
#### hab mal ein print eingefügt zum Testen(line 3), führt einfach mal test.py aus dann seht ihr den Print,
#### obwohl man nur importet.
##
if __name__ == "__main__":
    verbose = 0 ## falls 1, wird print mit port + info ausgegeben
    
    ports_dict = find_open_ports(dst_host="127.0.0.1", start_port=50, end_port=55, verbose=verbose)