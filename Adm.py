#/usr/bin/env python

import sqlite3
import datetime as dt
import os, sys, time
from colorama import init, Fore
import random as rd

init(autoreset=True)

red = Fore.RED
blue = Fore.BLUE
yellow= Fore.YELLOW
green = Fore.GREEN
purple = Fore.MAGENTA
gris = Fore.CYAN


try:
    os.remove("recover.py")
except Exception as e:
    pass

cleaner = "clear"

conexion = sqlite3.connect("recoveri.db")
cursor = conexion.cursor()
try:
    cursor.execute("""
        CREATE TABLE reiniciado(
            id VARCHAR(100) NOT NULL UNIQUE ,
            ip VARCHAR(100) NOT NULL,
            operador VARCHAR(100) NOT NULL,
            usuario VARCHAR(100) NOT NULL,
            contraseña VARCHAR(100) NOT NULL,
            dias INTEGER NOT NULL ,
            expiracion VARCHAR(100) NOT NULL

            )

        """)

except Exception as e:
    pass

def base_verificador():
    conexion = sqlite3.connect("recoveri.db")
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            CREATE TABLE identificador(
                ident INTEGER PRIMARY KEY AUTOINCREMENT,
                hardware VARCHAR(100) NOT NULL UNIQUE,
                rest_days INTEGER NOT NULL) """)

    except Exception as e:
        pass

conexion.commit()
conexion.close()

text = green + r""" 
      ______                              ________                                 
     /      \                            |        \                                
    |  $$$$$$\ _______    ______   _______\$$$$$$$$______    ______   ______ ____  
    | $$__| $$|       \  /      \ |       \ | $$  /      \  |      \ |      \    \ 
    | $$    $$| $$$$$$$\|  $$$$$$\| $$$$$$$\| $$ |  $$$$$$\  \$$$$$$\| $$$$$$\$$$$\
    | $$$$$$$$| $$  | $$| $$  | $$| $$  | $$| $$ | $$    $$ /      $$| $$ | $$ | $$
    | $$  | $$| $$  | $$| $$__/ $$| $$  | $$| $$ | $$$$$$$$|  $$$$$$$| $$ | $$ | $$
    | $$  | $$| $$  | $$ \$$    $$| $$  | $$| $$  \$$     \ \$$    $$| $$ | $$ | $$
     \$$   \$$ \$$   \$$  \$$$$$$  \$$   \$$ \$$   \$$$$$$$  \$$$$$$$ \$$  \$$  \$$

            [Code By:] MrAquiles
"""                                         

def slow_print(word):
    for w in word:
        sys.stdout.write(green + w)
        sys.stdout.flush()
        time.sleep(0.0005)

def ingresar(datos):
    conexion = sqlite3.connect("recoveri.db")
    cursor = conexion.cursor()

    try:
        cursor.executemany("INSERT INTO reiniciado VALUES (?,?,?,?,?,?,?)" , ([datos]))
        print(green + "\n##### Ejecucion completada ##### ")

    except sqlite3.IntegrityError:
        print(yellow + "ID ya REGISTRADO!!!!")

    except Exception as e:
        print(red + "Error, Datos mal puestos!! ")

    conexion.commit()
    conexion.close()

def mostrar_data():
    conexion = sqlite3.connect("recoveri.db")
    cursor = conexion.cursor()
    data = cursor.execute("SELECT * FROM reiniciado" ).fetchall()


    print(Fore.RED + "##### Claro ####")
    n = 1
    for usuario in data:
        if str(usuario[2])== "CLARO":
            rest_day = cursor.execute(f"SELECT rest_days FROM identificador WHERE hardware = '{usuario[0]}' ").fetchone()
            r = red + f"[{str(rest_day[0])}]"
            print(red + f"{usuario[0]}  ┼ {usuario[3]} ┼ ",r)
            n +=1 
          
    print(Fore.YELLOW + "\n##### Bitel ####")
    n2 = 1
    for usuario in data: 
        if str(usuario[2])== "BITEL":
            rest_day = cursor.execute(f"SELECT rest_days FROM identificador WHERE hardware = '{usuario[0]}' ").fetchone()
            r = red + f"[{str(rest_day[0])}]"
            print(yellow + f"{usuario[0]}  ┼ {usuario[3]} ┼ ", r)           
            n2 +=1 
            
    print(Fore.GREEN + "\n##### Movistar ####")
    n3 = 1
    for usuario in data:
        if str(usuario[2])== "MOVISTAR":
            rest_day = cursor.execute(f"SELECT rest_days FROM identificador WHERE hardware = '{usuario[0]}' ").fetchone()
            r = red + f"[{str(rest_day[0])}]"
            print(green + f"{usuario[0]}  ┼ {usuario[3]} ┼ ",r)           
            n3 +=1 


def consulta(id_de_hardware):

    conexion = sqlite3.connect("recoveri.db")
    cursor = conexion.cursor()

    try:
        datal = cursor.execute(f"SELECT * FROM reiniciado WHERE id = '{id_de_hardware}' ").fetchall()
        rest = cursor.execute(f"SELECT rest_days FROM identificador WHERE hardware = '{id_de_hardware}' " ).fetchone()
        rest_days = str(rest[0]).replace("-","")
    except Exception as e:
        pass
    else:
        try:
            print(green + "\n##### Ejecucion completada #####\n ")
            data = list(datal[0])
        #print(totdata)
            print(yellow + f"ID>\t\t{id_de_hardware}\nIP:\t\t{data[1]}\nOPERADOR:\t{data[2]}\nUSUARIO:\t{data[3]}\nCONTRASEÑA:\t{data[4]}\nDIAS:\t\t{data[5]}\nEXPIRACION:\t{data[6]}\nDIAS RESTANTES:\t{rest_days}")

        except Exception as i:
            print(red + "No se encontro informacion sobre ese ID! ")


    conexion.commit()
    conexion.close()

def actualizador(tabla, objeto, nuevobjeto, identificador):

    conex = sqlite3.connect("recoveri.db")
    cursor = conex.cursor()

    cursor.execute("UPDATE {} SET {} = '{}' WHERE Id = '{}' ".format(tabla, objeto, nuevobjeto,identificador))

    conex.commit()
    conex.close()

def daily_actualize():
    conex = sqlite3.connect("recoveri.db")
    cursor = conex.cursor()

    cursor.execute("DELETE FROM identificador") 
    time.sleep(1)
    cursor.execute("UPDATE {} SET seq = {} WHERE name = '{}' ".format("sqlite_sequence",0, "identificador" ))
    ids = cursor.execute("SELECT Id, expiracion FROM reiniciado").fetchall() 
    
    ahora = dt.datetime.now()
    t1 = dt.date(int(ahora.year),int(ahora.month),int(ahora.day))    
    try:
        for x in ids:
            t2 = dt.date(int(x[1][0:4]),int(x[1][5:6]),int(x[1][7:]))
            dias_restantes = t2 - t1
            #print(f"{x[0]} => {x[1][0:4]} {x[1][5:6]} {x[1][7:]}")
            cursor.execute("INSERT INTO identificador VALUES(null,'{}',{})".format(x[0], dias_restantes.days))

    except Exception as e:
        print(red + "Algo salio mall!!")
        print(red + "Error: ", e)
        print(red + "Contacta al Desarrollador!!!!")
        sys.exit()

    conex.commit()
    conex.close()

def eliminador():
    conex = sqlite3.connect("recoveri.db")
    cursor = conex.cursor()

    ahora = dt.datetime.now()
    t1 = dt.date(int(ahora.year),int(ahora.month),int(ahora.day))

    data_actual = cursor.execute("SELECT * FROM identificador").fetchall()
    print(r"/\ ELIMINADOR DE USUARIOS /\ " )
    for data in data_actual:
        id_to_consult = data[1]
        usuariot = cursor.execute(f"SELECT usuario FROM reiniciado WHERE Id = '{id_to_consult}' ").fetchone()

        if usuariot == None:
            continue
        
        r = red + "[{}]".format(str(data[2]).replace("-",""))
        print(green + f"[{data[0]}] ‡ {data[1]} ‡ {usuariot[0]} ‡ ",r)
    
    deleted = int(input("> "))
    try:
        point_identify = cursor.execute(f"SELECT hardware FROM identificador WHERE ident= {deleted}").fetchone()
        cursor.execute(f"DELETE FROM reiniciado WHERE Id = '{point_identify[0]}' ")
        time.sleep(1)


    except Exception as e:
        print(red + "ERROR: ", e)
        input(">")
    else:
        print(green + "#### OPERACION EJECUTADA ####")
        print(green + "\tChecking....")

    
    time.sleep(1)
    cursor.execute("DELETE FROM identificador") 
    conex.commit()
    conex.close()
    time.sleep(1)  

    conex = sqlite3.connect("recoveri.db")
    cursor = conex.cursor() 
    cursor.execute("UPDATE {} SET seq = {} WHERE name = '{}' ".format("sqlite_sequence",0, "identificador" ))
    ids = cursor.execute("SELECT Id, expiracion FROM reiniciado").fetchall() 
    try:
        for x in ids:
            t2 = dt.date(int(x[1][0:4]),int(x[1][5:6]),int(x[1][7:]))
            dias_restantes = t2 - t1
            #print(f"{x[0]} => {x[1][0:4]} {x[1][5:6]} {x[1][7:]}")
            cursor.execute("INSERT INTO identificador VALUES(null,'{}',{})".format(x[0], dias_restantes.days))

    except Exception as e:
        print(red + "Error: ", e)
        input("<ENTER>")
    else:
        print(yellow + "=$=$=$=$ Checked successfully!!! =$=$=$=$")
        input(green + "\n<ENTER> ")
    conex.commit()
    conex.close()

def update_identificador(numero, n_id):
    conex = sqlite3.connect("recoveri.db")
    cursor = conex.cursor()

    cursor.execute(f"UPDATE identificador SET hardware = '{n_id}' WHERE ident = ? ", numero)

    conex.commit()
    conex.close()

def data_for_identificador(id_hardware):
    conex = sqlite3.connect("recoveri.db")
    cursor = conex.cursor()

    now = dt.datetime.now()
    t1 = dt.date(int(now.year),int(now.month),int(now.day))
    x = cursor.execute(f"SELECT expiracion FROM reiniciado WHERE Id= '{id_hardware}' ").fetchone()

    t2 = dt.date(int(x[0][0:4]),int(x[0][5:6]),int(x[0][7:]))
    dias_restantes = t2 - t1

    cursor.execute("INSERT INTO identificador VALUES(null,'{}',{})".format(id_hardware, dias_restantes.days))

    conex.commit()
    conex.close() 

def menu_Actualizador():
    global lista

    conn = sqlite3.connect("recoveri.db")
    cursor = conn.cursor()
    os.system(cleaner)
    print(gris +"\t\t###################################")
    print(gris +"\t\t########## Actualizador ###########")
    print(gris +"\t\t###################################")

    opciones = """
        [1] Id de Hardware
        [2] Ip
        [3] Dias
        [4] Salir
    """

    print(gris + opciones)

    op = int(input("> "))

    if op == 1:
        print(blue + "Digite el ID DE HARDWARE a cambiar\n")
        ihar = input("> ")

        try:
            all_data = cursor.execute("SELECT * FROM reiniciado WHERE Id = '{}' ".format(ihar)).fetchone()
            less_data = cursor.execute(f"SELECT * FROM identificador WHERE hardware = '{ihar}' ").fetchone()
            identify = cursor.execute(f"SELECT ident FROM identificador WHERE hardware = '{ihar}'").fetchone()
            rest_time = cursor.execute(f"SELECT rest_days FROM identificador WHERE hardware = '{ihar}' ").fetchone()

            print(green + "==== Datos Actuales ====\n")
            print(green + f"[ID]\t\t\t{all_data[0]}\n[Usuario]\t\t{all_data[3]}\n[Dias Restantes]\t{less_data[2]}")

            if all_data == None:
                print(red + "No hay informacion sobre ese ID ")
                input(red + "<ENTER>")

            else:

                try:
                    print(green + "\n\tDigite el Nuevo ID \n")
                    new_id = input("> ").replace(" ","")

                    print(yellow +"\n1> claro\n2> bitel\n3> movistar")
                    ope = int(input("> "))

                    if ope == 1:
                        operador = "CLARO"

                    elif ope == 2:
                        operador = "BITEL"

                    elif ope == 3:
                        operador = "MOVISTAR"

                    else:
                        print("OPCION NULA ")

                    lista = [
                            "grifa",
                            "reiniciado",
                            "roto",
                            "inter"
                                 ]

                    palabra = rd.choice(lista)
                    usu = operador + new_id[0:5]
                    contrase = palabra + new_id[0:4]

                    #Actualizadores
                    actualizador("reiniciado","Id", new_id, ihar)
                    time.sleep(1)
                    actualizador("reiniciado","usuario", usu, new_id)
                    actualizador("reiniciado","contraseña", contrase, new_id)
                    time.sleep(1)
                    update_identificador(identify, new_id)

                    #Salida de informacion
                    print(green + "$$$$$ Ejecucion completada $$$$$")
                    print(yellow + "Obteniendo Info!!")
                    time.sleep(1)
                    print(green + f"[Id] {new_id}\n[Usuario] {usu}\n[Contraseña] {contrase}")
                    print(green + f"[Dias Restantes] {rest_time[0]}")

                    input(purple + "[ENTER] ")

                except Exception as i:
                    print(red + "Error: ",i)
                    input(red +"<ENTER> ")
                    os.system(cleaner)

        except Exception as e:
            print(red + "Error: ", e )
            input(red + "<ENTER> ")
            os.system(cleaner)

    elif op == 2:
        print(green  + "Digite el ID DE HARDWARE del cliente\n")
        id_to_change = input("> ")

        try:
            ipactual = cursor.execute("SELECT ip FROM reiniciado WHERE id = '{}'".format(id_to_change)).fetchone()
            print(yellow + f"\n\t#### [ID] {id_to_change} ! DIRECCION IP ACTUAL=> {ipactual[0]} ####\n")

            ip_to_Change = input(blue + "¿Cual es la nueva IP ?\n> ")

            try:
                actualizador("reiniciado","ip", ip_to_Change, id_to_change)
                print(green + "\n\t==== Ejecucion completada =====")
                input(purple + "[ENTER] ")

            except Exception as r:
                print(red + "Error: ",r)
                input(red +"<ENTER> ")

        except Exception as e:
            print(red + "Error: ",e)
            input(red + "<ENTER> ")




    elif op == 3:

        print(green + "Digite el ID DE HARDWARE del cliente\n")
        id_to_change5 = input("> ")

        try:
            dias_actuales = cursor.execute("SELECT dias, expiracion FROM reiniciado WHERE id = '{}'".format(id_to_change5)).fetchone()
            print(red + f"\n\t#### [ID] {id_to_change5}\n\t\tTotal de Dias Puestos => {dias_actuales[0]} Dias\n\t\tExpira => {dias_actuales[1]} ####\n")

            dias_to_Change = int(input(red + "\n¿Cuantos Dias seran puestos?\n> "))
            dias_propuestos = dt.timedelta(days=dias_to_Change)
            ahora = dt.datetime.now()
            expiracion = ahora + dias_propuestos
            formato_expiracion = "{}/{}/{}".format(expiracion.year, expiracion.month, expiracion.day)

            print(green + "\nNuevos datos:")
            print(gris + f"\n [ID] {id_to_change5}\n\tDias=> {dias_to_Change}\n\tExpira=> {formato_expiracion} ")

            try:
                actualizador("reiniciado","dias", dias_to_Change, id_to_change5)
                actualizador("reiniciado","expiracion", formato_expiracion, id_to_change5)

                time.sleep(1)

                t1 = dt.date(int(ahora.year),int(ahora.month),int(ahora.day))

                ids = cursor.execute(f"SELECT expiracion FROM reiniciado WHERE Id = '{id_to_change5}'").fetchone()
                t2 = dt.date(int(ids[0][0:4]),int(ids[0][5:6]),int(ids[0][7:]))
                dias_restantes = t2 - t1
                time.sleep(2)
                cursor.execute("UPDATE identificador SET rest_days = {} WHERE hardware = '{}' ".format(dias_restantes.days, id_to_change5))

                print(green + "\n\t==== Ejecucion completada =====")
                input(green + "[ENTER] ")

            except Exception as r:
                print(red + "Error: ",r)
                input(purple +"<ENTER> ")

        except Exception as e:
            print(red + "Error: ",e)
            input(purple + "<ENTER>")

    elif op == 4:
        print(green +"####################")
        print(green +"### Nos Vemos!!! ###")
        print(green +"####################")
        sys.exit()

    conn.commit()
    conn.close()
if __name__ == "__main__":
    base_verificador()
    daily_actualize()

    ipclaro= "45.79.48.104"
    ipmovistar = " 209.151.155.39"

    opciones = """
    1) Ingresar usuario recovery
    2) Consulta el ID
    3) Actualizar Datos
    4) Eliminar Usuarios
    5) Mostrar Detalles de usuarios
    6) Salir

    """
    bucle = True

    while bucle:
        os.system(cleaner)
        slow_print(text)
        tiempo = dt.datetime.now()
        print( Fore.GREEN + "=========================================================================================")
        print(Fore.RED + "Bienvenido Admin!! ")
        print(Fore.YELLOW + f"\t\t\t\t\t\t\t HOY => {tiempo.day}/{tiempo.month}/{tiempo.year}")
        print(yellow + opciones)
        op = int(input("> "))

        if op == 1:
            os.system(cleaner)

            id_har = input("ID > ")
            if id_har == "":
                print(red + "No coloco el ID de Hardware.")
                break
            else:
                pass

            print(yellow + "\n1> claro\n2> bitel\n3> movistar")
            ope = int(input("> "))

            if ope == 1:
                operador = "CLARO"
                ip_fija = ipclaro
            elif ope == 2:
                operador = "BITEL"
                ip_fija = ipmovistar
            elif ope == 3:
                operador = "MOVISTAR"
                ip_fija = ipmovistar
            else:
                print(red + "OPCION NULA ")

            usu = operador + id_har[0:5]
            contrase = "reiniciado" + id_har[0:4]
            dias = int(input("\nDIAS> "))
            dias_propuestos = dt.timedelta(days=dias)
            ahora = dt.datetime.now()
            expiracion = ahora + dias_propuestos
            formato_expiracion = "{}/{}/{}".format(expiracion.year, expiracion.month, expiracion.day)
            tupla_ingreso = (id_har, ip_fija, operador, usu, contrase, dias,  formato_expiracion)

            ingresar(tupla_ingreso)
            time.sleep(1)
            data_for_identificador(id_har)

            info = input(green + "\n\t ### Quieres ver su info ? ###  [y / n]> ")
            if info == "y" or info == "Y":
                consulta(id_har)
                input(green + "\n<ENTER>")

            else:
                pass

        elif op == 2:
            os.system(cleaner)

            print(blue + "Consulta el info del ID")
            id_consulta = input("> ")
            consulta(id_consulta)
            input(green + "\n<ENTER>")

        elif op == 3:
            os.system(cleaner)
            menu_Actualizador()

        elif op == 4:
            os.system(cleaner)
            eliminador()
        
        elif op == 5:
            os.system(cleaner)
            mostrar_data()
            input(green + "\n<ENTER>")

        elif op == 6:
            print(green +"\t####################")
            print(green +"\t### Nos Vemos!!! ###")
            print(green +"\t####################")
            sys.exit()

        else:
            print(red + "OPCION INVALIDA")
            sys.exit()
