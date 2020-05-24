from subprocess import Popen
import sys
import platform

num_of_clients = 4

processes = [Popen(['cmd.exe', '/c', 'start', 'python', 'client.py']) for msg in range(num_of_clients)]

for p in processes:
    p.wait()
