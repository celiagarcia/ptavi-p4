#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

try:
    # Dirección IP del servidor
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    # Contenido que vamos a enviar
    METODO = sys.argv[3]
    DIRECCION = sys.argv[4]
    EXPIRES = int(sys.argv[5])
except ValueError:
    sys.exit("Usage: client.py ip puerto register sip_address expires_value")
except IndexError:
    sys.exit("Usage: client.py ip puerto register sip_address expires_value")

if METODO == "register":
        LINE = 'REGISTER' + ' sip:' + DIRECCION + ' SIP/1.0\r\n\r\n'
        LINE += 'Expires: ' + str(EXPIRES) + '\r\n\r\n'

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print "Enviando: " + LINE
my_socket.send(LINE + '\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
