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

def register2file(clientes):
    #Vuelco el diccionario
    fich = open('registered.txt', 'w')
    fich.write('User\tIP\tExpires\r\n')
    for cliente in clientes:
        localhost = clientes[cliente][0][0]
        caducidad = int(clientes[cliente][1])
        cadena = cliente + '\t' + localhost + '\t'
        cadena += time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(caducidad)) + '\r\n'
        fich.write(cadena)

class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    def handle(self):
    
        #Actualizo el diccionario
        for cliente in clientes.keys():
            caducidad = int(clientes[cliente][1])
            if caducidad <= time.time():
                del clientes[cliente]

        # Escribe dirección y puerto del cliente (de tupla client_address)
        print self.client_address
        self.wfile.write("Hemos recibido tu peticion ")
        while 1:
         
            # Leyendo línea a línea lo que nos envía el cliente 
            line = self.rfile.read()
            if line != "":
                print "El cliente nos manda " + line       
                        
                #Guarda parámetros
                troceo = line.split()
                metodo = troceo[0]
                direccion = troceo[1].split(':')[1]
                expires = int(troceo[4])
                caducidad = time.time() + expires 
                      
                #REGISTER
                if metodo == 'REGISTER':
                    self.wfile.write('SIP/1.0 200 OK\r\n\r\n')
                    #Entra cliente
                    clientes[direccion] = [self.client_address, caducidad]
                    register2file(clientes)   
                    #Se da de baja cliente
                    if expires == 0:
                        del clientes[direccion]
                        register2file(clientes)
                print clientes        
            else:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[1])
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
    
