#/usr/bin/env python

import sqlite3
import datetime as dt 
import os, sys, time

cleaner = "clear"

conexion = sqlite3.connect("recoveri.db")
cursor = conexion.cursor()
try:
	cursor.execute("""
		CREATE TABLE reiniciado(
			id VARCHAR(100) NOT NULL,
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
	except Exception as e:
		print(f"ERROR => {e}")

	conexion.commit()
	conexion.close()

def consulta(id_de_hardware):

	conexion = sqlite3.connect("recoveri.db")
	cursor = conexion.cursor()

	datal = cursor.execute("SELECT * FROM reiniciado WHERE id = '{}' ".format(id_de_hardware)).fetchall()
	print("\n##### Ejecucion completada #####\n ")
	data = list(datal[0])
	#print(totdata)
	print(f"IP:\t\t{data[1]}\nOPERADOR:\t{data[2]}\nUSUARIO:\t{data[3]}\nCONTRASEÑA:\t{data[4]}\nDIAS:\t\t{data[5]}\nEXPIRACION:\t{data[6]}")

	#except Exception as e:
	#	print(f"ERROR => {e}")

	conexion.commit()
	conexion.close()


if __name__ == "__main__":

	ipclaro= "172.104.197.68"
	ipmovistar = "192.53.162.9"
	
	opciones = """
	1) Ingresar usuario recovery
	2) Consulta el ID
	3) Salir

	"""
	bucle = True

	while bucle:
		os.system(cleaner)
		print(opciones)
		op = int(input("> "))

		if op == 1:
			os.system(cleaner)

			id_har = input("ID > ")
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
			contrase = "reinicado" + id_har[0:4]
			dias = int(input("\nDIAS> "))
			dias_propuestos = dt.timedelta(days=dias)
			ahora = dt.datetime.now()
			expiracion = ahora + dias_propuestos
			formato_expiracion = "{}/{}/{}".format(expiracion.year, expiracion.month, expiracion.day)
			tupla_ingreso = (id_har, ip_fija, operador, usu, contrase, dias,  formato_expiracion)
			ingresar(tupla_ingreso)
			input("\n<ENTER>")

		elif op == 2:
			os.system(cleaner)

			print("Consulta el info del ID")
			id_consulta = input("> ")
			consulta(id_consulta)
			input("\n<ENTER>")

		elif op == 3:
			print("NOS VEMOS...")
			sys.exit()

		else:
			print("OPCION INVALIDA")
			sys.exit()
			