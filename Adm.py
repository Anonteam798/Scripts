#/usr/bin/env python

import sqlite3
import datetime as dt 
import os, sys, time

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

conexion.commit()
conexion.close()

def ingresar(datos):
	conexion = sqlite3.connect("recoveri.db")
	cursor = conexion.cursor()

	try:
		cursor.executemany("INSERT INTO reiniciado VALUES (?,?,?,?,?,?,?)" , ([datos]))
		print("\n##### Ejecucion completada ##### ")

	except sqlite3.IntegrityError:
		print("ID ya REGISTRADO!!!!")

	except Exception as e:
		print("Error, Datos mal puestos!! ")

	conexion.commit()
	conexion.close()

def consulta(id_de_hardware):

	conexion = sqlite3.connect("recoveri.db")
	cursor = conexion.cursor()

	datal = cursor.execute(f"SELECT * FROM reiniciado WHERE id = '{id_de_hardware}'").fetchall()
	print("\n##### Ejecucion completada #####\n ")
	data = list(datal[0])
	#print(totdata)
	print(f"ID>\t\t{id_de_hardware}\nIP:\t\t{data[1]}\nOPERADOR:\t{data[2]}\nUSUARIO:\t{data[3]}\nCONTRASEÑA:\t{data[4]}\nDIAS:\t\t{data[5]}\nEXPIRACION:\t{data[6]}")

	#except Exception as e:
	#	print(f"ERROR => {e}")

	conexion.commit()
	conexion.close()

def actualizador(obejeto, nuevobjeto, identificador):
	
	conex = sqlite3.connect("recoveri.db")
	cursor = conex.cursor()
	
	cursor.execute("UPDATE reiniciado SET {} = '{}' WHERE id = '{}' ".format(obejeto, nuevobjeto,identificador))

	conex.commit()
	conex.close()
	
def menu_Actualizador():

	conn = sqlite3.connect("recoveri.db")
	cursor = conn.cursor()

	print("\t\t###################################")
	print("\t\t########## Actualizador ###########")
	print("\t\t###################################")
			
	opciones = """
		[1] Id de Hardware
		[2] Ip
		[3] Operador
		[4] Usuario y Contraseña
		[5] Dias
		[6] Salir
	"""

	print(opciones)

	op = int(input("> "))

	if op == 1:
		print("Digite el ID DE HARDWARE a cambiar\n")
		ihar = input("> ")

		try:
			deta = cursor.execute("SELECT * FROM reiniciado WHERE id = '{}'".format(ihar)).fetchone()
			
			if deta == None: 
				print("No hay informacion sobre ese ID ")

			else:

				try:
					print("\n\tDigite el Nuevo ID \n")
					new_id = input("> ")
					actualizador("id", new_id, ihar)
					print("Ejecucion completada")
					input("[ENTER] ")

				except Exception as i:
					print("Error: ",i)

		except Exception as e:
			print("Error: ", e )

	elif op == 2:
		print("Digite el ID DE HARDWARE del cliente\n")
		id_to_change = input("> ")

		try:
			ipactual = cursor.execute("SELECT ip FROM reiniciado WHERE id = '{}'".format(id_to_change)).fetchone()
			print(f"\n\t#### [ID] {id_to_change} ! DIRECCION IP ACTUAL=> {ipactual[0]} ####\n")

			ip_to_Change = input("¿Cual es la nueva IP ?\n> ")

			try:
				actualizador("ip", ip_to_Change, id_to_change)
				print("\n\t==== Ejecucion completada =====")
				input("[ENTER] ")

			except Exception as r:
				print("Error: ",r)

		except Exception as e:
			print("Error: ",e)

	elif op == 3:

		print("Digite el ID DE HARDWARE del cliente\n")
		id_to_change3 = input("> ")

		try:
			actual_operador  = cursor.execute("SELECT operador  FROM reiniciado WHERE id = '{}'".format(id_to_change3)).fetchone()
			print(f"\n\t#### [ID] {id_to_change3} ! Operador ACTUAL=> {actual_operador[0]} ####\n")

			operador_to_change = input("¿Cual es el nuevo operador ?\n> ").upper()

			try:
				actualizador("operador", operador_to_change, id_to_change3)
				print("\n\t==== Ejecucion completada =====")
				input("[ENTER] ")

			except Exception as r:
				print("Error: ",r)

		except Exception as e:
			print("Error: ",e)

	elif op == 4:

		print("Digite el ID DE HARDWARE del cliente\n")
		id_to_change4 = input("> ")

		try:
			credenciales  = cursor.execute("SELECT usuario, contraseña  FROM reiniciado WHERE id = '{}'".format(id_to_change4)).fetchone()
			print(f"\n\t#### [ID] {id_to_change4} ! Usuario ACTUAL=> {credenciales[0]}\n\t\t\t\t\t\t    Contraseña Actual=> {credenciales[1]} ####\n")

			usuario_to_Change = input("¿cual es el nuevo usuario ?\n> ").capitalize()
			contraseña_to_change = input("\n¿Cual es la nueva contraseña?\n> ")

			try:
				actualizador("usuario", usuario_to_Change, id_to_change4)
				actualizador("contraseña", contraseña_to_change, id_to_change4 )
				print("\n\t==== Ejecucion completada =====")
				input("[ENTER] ")

			except Exception as r:
				print("Error: ",r)

		except Exception as e:
			print("Error: ",e)

	elif op == 5:
		print("Digite el ID DE HARDWARE del cliente\n")
		id_to_change5 = input("> ")

		try:
			dias_actuales = cursor.execute("SELECT dias, expiracion FROM reiniciado WHERE id = '{}'".format(id_to_change5)).fetchone()
			print(f"\n\t#### [ID] {id_to_change5}\n\t\tTotal de Dias Puestos => {dias_actuales[0]} Dias\n\t\tExpira => {dias_actuales[1]} ####\n")

			dias_to_Change = int(input("\n¿Cuantos Dias seran puestos?\n> "))
			dias_propuestos = dt.timedelta(days=dias_to_Change)
			ahora = dt.datetime.now()
			expiracion = ahora + dias_propuestos
			formato_expiracion = "{}/{}/{}".format(expiracion.year, expiracion.month, expiracion.day)

			print("\nNuevos datos:")
			print(f"\n [ID] {id_to_change5}\n\tDias=> {dias_to_Change}\n\tExpira=> {formato_expiracion} ")

			try:
				actualizador("dias", dias_to_Change, id_to_change5)
				actualizador("expiracion", formato_expiracion, id_to_change5)
				print("\n\t==== Ejecucion completada =====")
				input("[ENTER] ")

			except Exception as r:
				print("Error: ",r)
				input("x ")

		except Exception as e:
			print("Error: ",e)
			input("E")

	elif op == 6:
		print("Nos Vemos!!! ")
		sys.exit()

	conn.commit()
	conn.close()
if __name__ == "__main__":

	ipclaro= "45.79.48.104"
	ipmovistar = "209.151.155.39"
	
	opciones = """
	1) Ingresar usuario recovery
	2) Consulta el ID
	3) Actualizar Datos
	4) Salir

	"""
	bucle = True

	while bucle:
		os.system(cleaner)
		print(opciones)
		op = int(input("> "))

		if op == 1:
			os.system(cleaner)

			id_har = input("ID > ")
			if id_har == "":
				print("No coloco el ID de Hardware.")
				break 
			else:
				pass

			print("\n1> claro\n2> bitel\n3> movistar")
			ope = int(input("> "))
			
			if ope == 1:
				operador = "CLARO"
				ip_fija = ipclaro
			elif ope == 2:
				operador = "BITEL"
				ip_fija = ipclaro
			elif ope == 3:
				operador = "MOVISTAR"
				ip_fija = ipmovistar
			else:
				print("OPCION NULA ")

			usu = operador + id_har[0:5]
			contrase = "reiniciado" + id_har[0:4]
			dias = int(input("\nDIAS> "))
			dias_propuestos = dt.timedelta(days=dias)
			ahora = dt.datetime.now()
			expiracion = ahora + dias_propuestos
			formato_expiracion = "{}/{}/{}".format(expiracion.year, expiracion.month, expiracion.day)
			tupla_ingreso = (id_har, ip_fija, operador, usu, contrase, dias,  formato_expiracion)
			
			ingresar(tupla_ingreso)
			
			info = input("\n\t ### Quieres ver su info ? ###  [y / n]> ")
			if info == "y" or info == "Y":
				consulta(id_har)
				input("\n<ENTER>")

			else:
				pass

		elif op == 2:
			os.system(cleaner)

			print("Consulta el info del ID")
			id_consulta = input("> ")
			consulta(id_consulta)
			input("\n<ENTER>")

		elif op == 3: 
			os.system(cleaner)
			menu_Actualizador()

		elif op == 4:
			print("NOS VEMOS...")
			sys.exit()

		else:
			print("OPCION INVALIDA")
			sys.exit()
			
