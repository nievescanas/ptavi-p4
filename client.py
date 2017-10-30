#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""
import sys
import socket
import urllib.request

LINE = ' '

try:
    numtime = sys.argv[5]
except IndexError:
    sys.exit("Usage: client.py ip puerto register sip_address expires_value")

if sys.argv[3] == 'register':
    LINE = str.upper(sys.argv[3]) + ' sip:' + sys.argv[4] + ' SIP/2.0\r\n'
    LINE += 'Expires: ' + sys.argv[5] + '\r\n\r\n'

elif sys.argv[3] == 'REGISTER':
    for palabra in sys.argv[3:]:
        LINE += ('{p}{espacio}'.format(p=palabra, espacio=' '))

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((sys.argv[1], int(sys.argv[2])))
    print("Enviando:", LINE)
    my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
