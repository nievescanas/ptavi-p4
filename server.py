#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""
import sys
import socketserver
import json
import time


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    c_dicc = {}

    def register2json(self, name='registered.json'):
        with open(name, 'w') as outfile:
            json.dump(self.c_dicc, outfile, separators=(',', ':'), indent="")

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        self.wfile.write(b"Hemos recibido tu peticion")
        for line in self.rfile:
            if not line or line.decode('utf-8') == "\r\n":
                continue
            else:
                print("El cliente nos manda ", line.decode('utf-8'))
                metodo = (line.decode('utf-8').split())
                ip = self.client_address[0]

                if metodo[0] == 'REGISTER':
                    correo = metodo[1][metodo[1].rfind(':')+1:]
                    self.wfile.write(b' SIP/2.0 200 OK\r\n\r\n')

                elif metodo[0] == 'Expires:':
                    if metodo[1] > '0':
                        caducidad = time.ctime(time.time() + int(metodo[1]))
                        info = [ip, caducidad]
                        self.c_dicc[correo] = info

                    elif metodo[1] == '0':
                        del self.c_dicc[correo]

                lista = [self.c_dicc]
                print(lista)

        for posicion in lista:
            for dicc in posicion:
                caducidad = self.c_dicc[dicc][1]
                now = time.ctime(time.time())
                if caducidad <= now:
                    del self.c_dicc[dicc]
                    break

        def register2json(self, name='registered.json'):
            with open(name, 'w') as outfile:
                json.dump(self.c_dicc, outfile, separators=(',', ':'))

        print(self.client_address)
        self.register2json()


if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', 5060), SIPRegisterHandler)

    print("Lanzando servidor UDP de eco...")

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
