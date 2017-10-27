#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""
import sys
import socketserver


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    class_dicc = {}

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.wfile.write(b"Hemos recibido tu peticion")
        for line in self.rfile:
            print("El cliente nos manda ", line.decode('utf-8'))
            
            metodo = (line.decode('utf-8').split())
            ip = self.client_address[0]
            dicc = {}

            if metodo[0] == 'REGISTER'and metodo[2] == 'SIP/2.0\r\n\r\n':
                direccion = metodo[1][metodo[1].rfind(':')+1:]
                self.class_dicc[ip] = direccion
                self.wfile.write(b' SIP/2.0 200 OK\r\n\r\n')               
        print(self.client_address)
        


if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', 5060), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
