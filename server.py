#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time

clientes = {}


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    def handle(self):
        """
        Actualiza y modifica el diccionario cada vez que recibe REGISTER
        """
        #Actualizo el diccionario
        for cliente in clientes.keys():
            caducidad = int(clientes[cliente][1])
            if caducidad <= time.time():
                del clientes[cliente]
        print self.client_address
        self.wfile.write("Hemos recibido tu peticion ")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if line != "":
                print "El cliente nos manda " + line

                troceo = line.split()
                metodo = troceo[0]
                direccion = troceo[1].split(':')[1]
                expires = int(troceo[4])
                caducidad = time.time() + expires

                #REGISTER
                if metodo == 'REGISTER':
                    self.wfile.write('SIP/2.0 200 OK\r\n\r\n')
                    #Entra cliente
                    clientes[direccion] = [self.client_address, caducidad]
                    self.register2file(clientes)
                    #Se da de baja cliente
                    if expires == 0:
                        del clientes[direccion]
                        self.register2file(clientes)
            else:
                break

    def register2file(self, clientes):
        """
        Vuelca el diccionario en el fichero registered.txt
        """
        fich = open('registered.txt', 'w')
        fich.write('User\tIP\tExpires\r\n')
        for cliente in clientes:
            localhost = clientes[cliente][0][0]
            caduc = int(clientes[cliente][1])
            cadena = cliente + '\t' + localhost + '\t'
            cadena += time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(caduc))
            cadena += '\r\n'
            fich.write(cadena)

if __name__ == "__main__":
    """
    Creamos servidor de eco y escuchamos
    """
    PORT = int(sys.argv[1])
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
