#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys

clientes = {}

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
    
        # Escribe dirección y puerto del cliente (de tupla client_address)
        print self.client_address
        self.wfile.write("Hemos recibido tu peticion ")
        
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente 
            line = self.rfile.read()
            if line != "":
                print "El cliente nos manda " + line
                #Trocea el mensaje
                troceo = line.split()
                metodo = troceo[0]
                direccion = troceo[1]
                expires = int(troceo[4])        
                #Guarda la dirección del cliente en el diccionario
                if metodo == 'REGISTER':
                    clientes[direccion] = self.client_address
                #Borra la direccion del cliente si expire=0
                if expires == 0:
                    del clientes[direccion]
                #Responde al cliente
                    self.wfile.write('SIP/1.0 200 OK\r\n\r\n')               
            else:
                break
        print clientes
        
if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[1])
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
    
