# primenjeni_dist_sys_zad1
Domaći zadatak iz primenjenih distribuiranih sistema koristeći Zookeeper

Koristi python 3.8 i kazoo biblioteku za komunikaciju sa zookeeper-om

Koraci za pokretanje (iz konzole):

1. Instalirati python ako ga već nemate
2. Napraviti venv komandom: python -m venv venv
3. Aktivrati venv sa: venv\Scripts\activate
4. Instalirati kazoo sa: pip install kazoo
5. pokrenuti main skriptu sa: python main.py

Otvoriće se 4 prozora sa konzolama svakog od Zookeeper klijenata, 
koji će izmedju sebe izabrati leadera i sačekati 100 sekundi pre izlaska.
