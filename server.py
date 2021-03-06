#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""
import sys
import socketserver
import json
import time
import os.path as path


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    c_dicc = {}

    """
    Comprueba si existe el fichero y lo utiliza como diccionario
    """
    def json2registered(self):
        if path.exists('registered.json'):
            with open('registered.json') as d_file:
                data = json.load(d_file)
                self.c_dicc = data
    """
    Crea y escribe un fichero json
    """

    def register2json(self, name='registered.json'):
        with open(name, 'w') as outfile:
            json.dump(self.c_dicc, outfile, separators=(',', ':'), indent="")
    """
    Comprueba y borra los usuarios caducados
    """

    def caducidad(self):
        tmp_list = []
        for usuario in self.c_dicc:
            caducidad = self.c_dicc[usuario][1]
            now = time.ctime(time.time())
            if caducidad <= now:
                tmp_list.append(usuario)
        for usuario in tmp_list:
            del self.c_dicc[usuario]

    def handle(self):
        """
        handle method of the server class
        (all requests will be handled by this method)
        """
        if not self.c_dicc:
            self.json2registered()

        for line in self.rfile:
            if not line or line.decode('utf-8') == "\r\n":
                continue
            else:
                metodo = (line.decode('utf-8').split())
                ip = self.client_address[0]
                self.caducidad()

                if metodo[0] == 'REGISTER':
                    correo = metodo[1][metodo[1].rfind(':')+1:]
                    self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')

                elif metodo[0] == 'Expires:':
                    if metodo[1] > '0':
                        caducidad = time.ctime(time.time() + int(metodo[1]))
                        info = [ip, caducidad]
                        self.c_dicc[correo] = info

                    elif metodo[1] == '0':
                        if correo in self.c_dicc:
                            del self.c_dicc[correo]

                self.register2json()

        print(self.client_address)


if __name__ == "__main__":
    # Listens at localhost ('') port 6001
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', 5060), SIPRegisterHandler)

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
