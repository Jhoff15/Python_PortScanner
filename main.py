import logging
from time import perf_counter
from port_scanner import find_all_async
from helper import get_system32_services_dict, get_inputs, create_file_name

##
## Ausgangspunkt des Programms, bewusst knapp gehalten -> best Practice für exe
##
def main():
    # Counter um Programmlaufzeit zu bestimmen
    t1 = perf_counter()

    ########### Inputs #############
    # Helper-Input Funktion für Eingabe von:
    # Host-IP -> dst_host
    # Erster Port -> start_port
    # Letzter Port -> end_port
    dst_host, start_port, end_port = get_inputs()
    ################################

    # 2. Counter um Programmlaufzeit ohne Input zu bestimmen
    t2 = perf_counter()

    # Starte Asynchrone Abfrage der Ports
    open_ports = find_all_async(dst_host=dst_host, start_port=start_port, end_port=end_port)
    # Sortiere Ports für aufsteigende Auflistung
    open_ports.sort()
    # Gebe sortierte Ports aus
    print(f'open_ports returned: {open_ports}')

    # Erzeuge ein Dictionary(Java: HashMap) der Standart Port Belegung {key: value} => {port: service}
    services_dict = get_system32_services_dict()

    # Erzeuge Logger und dessen File
    file_name = create_file_name()
    logging.basicConfig(filename=file_name, encoding='utf-8', level=logging.DEBUG)

    # Ordne offenen Ports einem Service zu und schreibe in die Logger Datei
    for port in open_ports:
        try:
            logging.info(f"   Offener Port: {port}, Protokoll: tcp, Protokoll: {services_dict.get(port)}")
        except TypeError as e:
            logging.error(f"   Port {port} offen, aber nicht in Protokoll: {e}")

    # 3. Counter speichert Zeit zum Ende der Programmlaufzeit
    t3 = perf_counter()
    # Gebe Programmlaufzeit aus.
    print(f'Complete Execution Time: \t {t3-t1}')
    print(f'Programm Execution Time: \t {t3-t2}')

if __name__ == "__main__":
    main()