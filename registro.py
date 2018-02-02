import sys
import os

from conexion import Conexion


class Empleado(object):

	"""def registroEmpleado(self, cedula, nombres, apellidos, fecha, edad, aportaciones, dir1, 
		dir2, telf1, telf2, email, sueldo, diasLabor, sexo, nivelAcad, cuentaBamc, tipoDisc, 
		nombreRec, telfRec, celRec, ciudad, foto):
		print(conexionDB(self))
		if conexionDB(self):
			print('Registrado')
			cursor = con.cursor()
			cursor.execute("INSERT INTO empleado (cedula, nombres, apellidos, fecha_nacimiento, edad, numero_aportaciones, direccion1, direccion2,"
				"telefono1, telefono2, email, sueldo, dias_laborales, sexo_oid, nivel_academico_oid, numero_cuenta_bancaria, tipo_discapacidad_oid,"
				"nombre_recomendado, telefono_recomendado, celular_recomendado, ciudad, foto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
				[cedula, nombres, apellidos, fecha, edad, aportaciones, dir1, dir2, telf1, telf2, email, sueldo, diasLabor, 
				sexo, nivelAcad, cuentaBamc, tipoDisc, nombreRec, telfRec, celRec, ciudad, foto])
			self.con.commit()
			cursor.close()
			self.con.close()
		else:
			return False
	"""
	#print(registroEmpleado('','','','','','','','','','','','','','','','','','','','','','',''))
	def registroEmpleado(self, cedula, nombres, apellidos, fecha, edad, aportaciones, dir1, 
		dir2, telf1, telf2, email, sueldo, diasLabor, sexo, nivelAcad, cuentaBamc, tipoDisc, 
		nombreRec, telfRec, celRec, ciudad, foto):
		c = Conexion.conexionDB(self)
		cursor = c.con.cursor()
		cursor.execute("INSERT INTO empleado (cedula, nombres, apellidos, fecha_nacimiento, edad, numero_aportaciones, direccion1, direccion2,"
			"telefono1, telefono2, email, sueldo, dias_laborales, sexo_oid, nivel_academico_oid, numero_cuenta_bancaria, tipo_discapacidad_oid,"
			"nombre_recomendado, telefono_recomendado, celular_recomendado, ciudad, foto) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
			[cedula, nombres, apellidos, fecha, edad, aportaciones, dir1, dir2, telf1, telf2, email, sueldo, diasLabor, 
			sexo, nivelAcad, cuentaBamc, tipoDisc, nombreRec, telfRec, celRec, ciudad, foto])
		self.con.commit()
		cursor.close()
		self.con.close()

	registroEmpleado('','','','','','','','','','','','','','','','','','','','','','','')

		
		