#!/usr/bin/python
#-*- coding:UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import httplib
import urllib
from termcolor import colored
import json
from datetime import datetime
import sys

# definimos la hora 
fecha = datetime.now()
hora  = '%s/%s/%s a las %s:%s:%s' % (fecha.day, fecha.month, fecha.year, fecha.hour, fecha.minute, fecha.second)

# Mensaje de inicio
print colored("""
                   ╔═══╗  ╔╗        ╔╗
                   ╚╗╔╗║ ╔╝╚╗       ║║
                    ║║║╠═╩╗╔╬══╦══╦═╝╠══╦═╗
                    ║║║║╔╗║║║║═╣╔╗║╔╗║╔╗║╔╝
                   ╔╝╚╝║╔╗║╚╣║═╣╔╗║╚╝║╚╝║║
                   ╚═══╩╝╚╩═╩══╩╝╚╩══╩══╩╝
                      v1.1 by @unkndown
""","blue", attrs=['bold'])
# Opciones
print colored(" Obtén los datos de una persona con el rut o nombre de ella: \n\n -Ejemplo con rut: 5519653-2 \n -Ejemplo con nombre: Pedro Aguilar Toloza\n -Si tienes solo una parte del nombre, usa la opción stalker\n", "magenta", attrs=['bold'])

# Iniciamos la ejecución
try:

    #
    # Obtenemos el rut a partir del dato que nos de el usuario
    #

    nombre     = raw_input(" Ingresa un rut o nombre: ")
    print colored(" \n [+] Buscando datos \n","green",attrs =['bold'])
    link       = "https://chile.rutificador.com/get_generic_ajax/"
    host       = "chile.rutificador.com:80"
    headers    = {'Origin': 'https://chile.rutificador.com','Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'es-ES,es;q=0.8', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': '*/*', 'Referer': 'https://chile.rutificador.com/', 'X-Requested-With': 'XMLHttpRequest', 'Connection': 'keep-alive', }
    cookies    = {'_gat': '1', 'csrftoken': 'W9s4ydeFOSbl37Gp3iYnOMDBIGbYz7AW', '_ga': 'GA1.2.62259178.1488421266', }
    parametros = {'csrfmiddlewaretoken': 'W9s4ydeFOSbl37Gp3iYnOMDBIGbYz7AW', 'entrada': nombre }
    respuesta  = requests.post('https://chile.rutificador.com/get_generic_ajax/', headers=headers, cookies=cookies, data=parametros)
    ver_source = respuesta.text
    data       = json.loads(ver_source)

    # verificamos si se ha encontrado un dato 
    if data['status'] != "not_found":
        # verificamos si se ha pasado un parametro
        if len(sys.argv) >= 2:
            # verificamos si el parametro es stalker
            if sys.argv[1] == "stalker":
                print colored("+------------------------------------------+","green", attrs=['bold'])
                # contamos los registros encontrados 
                total = len(data['value'])
                # abrimos el archivo datos.txt o lo creamos si no existe para guardar el resultado de la búsqueda
                txt = open('datos.txt', 'a')
                datos = ""
                datos += "+------------------------------------------+\n"
                # mostramos la fecha de la búsqueda
                datos += "         " + hora + "\n"
                datos += "+------------------------------------------+\n"
                # mostramos los datos encontrados
                for i in range(1, total):
                    nombre = data['value'][i]['name']
                    rut    = str(data['value'][i]['rut']) + "-" + str(data['value'][i]['dv'])
                    datos  += u' - '.join((nombre,rut)).encode('utf-8').strip() + "\n"
                    print colored(" Nombre: ","blue", attrs=['bold']) + nombre + "\n" + colored(" Rut: ","blue", attrs=['bold']) + rut
                    print colored("+------------------------------------------+","green", attrs=['bold'])
                # guardamos los datos en el archivo txt
                txt.write(datos)
                txt.close()
                exit()
            else:
                # si la opción es diferente de stalker, mostramos un error
                print colored("\n\n  Usa un comando valido \n","red", attrs=['bold'])
                exit()

        # definimos el rut
        rut = str(data['value'][0]['rut']) + str(data['value'][0]['dv'])
        print colored("+------------------------------------------+","green", attrs=['bold'])
        print " Rut usuario: " + rut

        # 
        # Obtenemos la información a partir del rut obtenido
        # 
        url     = "http://buscardatos.com/cl/personas/padron_cedula_chile.php"
        hosts   = "buscardatos.com:80"
        post    = urllib.urlencode({'cedula': rut})
        conex   = httplib.HTTPConnection(hosts)
        conex.request("POST", url, post, headers)
        request = conex.getresponse()

        # verificamos si el status de nuestra peticion es 200
        if request.status == 200:
            respuesta = request.read()
            html      = BeautifulSoup(respuesta,"html5lib")
            entradas  = html.find_all('tr')
            txt       = open('datos.txt', 'a')
            datos     = ""
            datos     += "+------------------------------------------+\n"
            datos     += "         " + hora + "\n"
            datos     += "+------------------------------------------+\n"

            # mostramos la información
            for item in entradas:
                item.encode('utf-8')
                resultado  = item.getText()
                reemplazar = resultado.replace(">","")
                separar    = reemplazar.split(":",1)
                datos      += u' '.join((' ',reemplazar)).encode('utf-8').strip() + "\n"
                print colored("+------------------------------------------+","green", attrs=['bold'])
                print  str(" ") + colored(separar[0],"blue", attrs=['bold']) + str(":") + separar[1]
            # guardamos los datos en el archivo txt
            txt.write(datos)
            txt.close()
            print colored("+------------------------------------------+","green", attrs=['bold'])
            print colored("\n [+] No se han encontrado mas datos\n","red",attrs=['bold'])
        else:
            # si la respuesta no es 200 mostramos un error de conexion
            print colored("\n\n  Error en la conexion \n","red", attrs=['bold'])
        conex.close()
    else:
        # si no se ha encontrado al menos una persona mostramos un mensaje de error
        print colored(" [-] No se ha encontrado informacion\n","red",attrs=['bold'])

# Si cancela la ejecución, mostramos un mensaje de despedida
except KeyboardInterrupt:
    print colored("\n\n Ejecucion cancelada, hasta la proxima\n","red",attrs=['bold'])
