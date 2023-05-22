# Python_PortScanner
Portscanner für das IT-Sicherheit Labor im SS23.
Der Branch Basic ist die von Professorin Kiss gegebene Grundlage und wurde leicht verändert.
In diesem Branch wird die Basis ausführlich erklärt.

Der Main-Branch beinhaltet unsere Lösung. In der Lösung wurde Multithreading benutzt um die 
Performance zu steigern und anstatt der connect() Funktion aus der Socket Libary, wo möglich die
connect_ex() Funktion aus der gleichen Libary verwendet. So können try-catch Blöcke vermieden werden
und die Programmlaufzeit vermindert sich weiter.

## Branches
+ main -> Main Branch, Abgabe für Labor
+ basic -> Beschreibung und Anpassung (für Best Practices) des vorgegebenen Basiscodes

## Weiterentwicklung
Möchte man einen fortgeschritteneren PortScanner bauen, so sollte man sich zwei Tools genauer Ansehen. 

Zum einen gibt es die Möglichkeit Scapy in Python einzubinden und so genauere Details von einem Host und dessen offenen Ports zu erlangen, oder man nutzt ein tool Namens nmap. 
Dieses sehr mächtige Tool macht es einem sehr schnell, ohne große Vorkenntnisse, möglich einen Host auf schwachstellen zu untersuchen. 
Nmap oder das Nmap Tool Zenmap zeigen einem Versionsnummern zu verwendeten Services sowie weitere Infos über einen Host an. Ist
ein System schlecht konfiguriert bekommt man sogar das Betriebssystem des Hosts raus. 

Egal ob Scapy oder nmap mit diesen fertigen Tools können Scripte entwickelt werden, die Ports und deren Services mit großer
genauigkeit herausfinden und sogar automatisiert Schwachstellen von den jeweiligen Services (und deren Versionen) angreifen.
