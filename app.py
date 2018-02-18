"""Aplicación de Registro de Estudiantes
Creado el 25 de Enero de 2018
@author: Pablo España B.
"""

import sys
import os
import sqlite3
import datetime
import cv2 # Descargado opencv-python
from PyQt5 import uic, QtWidgets, QtGui, QtCore #importamos uic y QtWidgets desde el modulo PyQt5
from random import randint
import psycopg2 # Descargado
import qdarkstyle # Descargado



qtCreatorFile = "diseño.ui"
if not os.path.exists('fotos'): os.makedirs('fotos')

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile) # usammos loadUiType para cargar el diseño de qt creator

class Estudiante(QtWidgets.QMainWindow, Ui_MainWindow):  # Creamos nuestra clase con sus parametros (QtWidgets.QMainWindow y el diseño de qt creator
	"""Este clase contiene los metodos para el manejo de registro de estudiantes"""
	def __init__(self):             # Metodos init para iniciar la aplicacion
		"""Metodo constructor de la clase"""
		QtWidgets.QMainWindow.__init__(self) # Preparamos una ventana principal
		Ui_MainWindow.__init__(self) # Iniciar el diseño de qt creator
		self.setupUi(self)  # Inicializamos la configuracion de la interfaz
		self.setWindowTitle(u"Gestión de empleados")
		
		self.host = 'localhost'
		self.dbname = 'DB_Empleados'
		self.user = 'postgres'
		self.password = '12345'

		self.image = None
		self.selecciona = False
		self.fotoNueva = None
		########## VALIDACIONES DE CAMPOS ##############
		self.soloNumeros = QtGui.QIntValidator()
		self.txtCedula.setValidator(self.soloNumeros)
		self.txtTelefono1.setValidator(self.soloNumeros)
		self.txtTelefono2.setValidator(self.soloNumeros)
		self.txtTelefonoRecom.setValidator(self.soloNumeros)
		self.txtCelularRecom.setValidator(self.soloNumeros)
		###############################################

		self.btnBuscarImg.clicked.connect(self.buscarImagen) # evento producido cuando se selecciona un elemento
		self.btnGuardar.clicked.connect(self.registrarEmpleado) # Id del boton conectado a la funcion guardarCliente
		self.btnBuscar.clicked.connect(self.buscarEmpleado) # Id del boton conectado a la funcion guardarCliente
		self.btnLimpiar.clicked.connect(self.borrarCampos) # Id del boton conectado a la funcion guardarCliente
		self.btnEliminar.clicked.connect(self.eliminarEmpleado) # Id del boton conectado a la funcion guardarCliente
		self.listaEmpleados.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows) # seleccionar solo filas
		self.listaEmpleados.setSelectionMode(QtWidgets.QTableWidget.SingleSelection) # usar seleccion simple, una fila a la vez
		self.listaEmpleados.itemPressed.connect(self.seleccionarFila) # evento producido cuando se selecciona un elemento
		self.btnEliminar.setEnabled(False)
		 # Conexión a la base de datos creada en postgres
		self.conexionDB()
		self.mostrarEmpleados()
		

	def closeEvent(self, event):
		"""Este metodo nos permite confirmar el cierre de una ventana"""
		cerrar = QtWidgets.QMessageBox.question(self, "Salir", "¿Seguro que quieres salir de la aplicación?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		if cerrar == QtWidgets.QMessageBox.Yes:
			event.accept()
		else: event.ignore()
			
	def conexionDB(self):
		conn_string = "host={0} user={1} dbname={2} password={3}".format(self.host, self.user, self.dbname, self.password)
		self.con = psycopg2.connect(conn_string)
		print("Conexión establecida")
		self.cursor = self.con.cursor()
		#self.cursor.execute("INSERT INTO empleado (cedula) VALUES (%s);", [434])
		#self.con.commit()
		#self.cursor.close()
		self.con.close()

	def registrarEmpleado(self):
		conn_string = "host={0} user={1} dbname={2} password={3}".format(self.host, self.user, self.dbname, self.password)
		self.con = psycopg2.connect(conn_string)
		self.cursor = self.con.cursor()
		self.id = self.txtID.text()
		self.cedula = self.txtCedula.text()
		self.nombres = str(self.txtNombres.text())
		self.apellidos = str(self.txtApellidos.text())
		self.fecha = str(self.txtFecha.text())
		self.edad = self.txtEdad.text()
		self.aportaciones = self.txtAport.text()
		self.dir1 = str(self.txtDireccion1.text())
		self.dir2 = str(self.txtDireccion2.text())
		self.telf1 = str(self.txtTelefono1.text())
		self.telf2 = str(self.txtTelefono2.text())
		self.email = str(self.txtCorreo.text())
<<<<<<< HEAD
		#self.sueldo = self.txtSueldo.text()
=======
>>>>>>> da595147fd2d80fb1889723708df79f6bbc86862
		self.sueldo = self.txtSueldo.text().replace(",",".")
		self.diasLabor = self.txtDias.text()
		self.sexo = str(self.cbxSexo.currentText())
		self.nivelAcad = str(self.cbxNivel.currentText())
		self.cuentaBamc = str(self.txtCuenta.text())
		self.tipoDisc = str(self.cbxDiscapacidad.currentText())
		self.nombreRec = str(self.txtNombreRecom.text())
		self.telfRec = str(self.txtTelefonoRecom.text())
		self.celRec = str(self.txtCelularRecom.text())
		self.ciudad = str(self.txtCiudad.text())
		self.verificar(self.cedula)
		if self.verificar(self.cedula):
			if  self.btnGuardar.text() == 'Guardar':
				if self.selecciona:
						self.guardarImagen()
				else:
					self.fname = "Ninguna"
				self.cursor.execute("INSERT INTO empleado (cedula, nombres, apellidos, fecha_nacimiento, edad, numero_aportaciones, direccion1,"
					"direccion2, telefono1, telefono2, email, sueldo, dias_laborales, genero, nivel_academico, numero_cuenta_bancaria, tipo_discapacidad,"
					"nombre_recomendado, telefono_recomendado, celular_recomendado, ciudad, foto)"
					" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s, %s);", 
					[self.cedula, self.nombres, self.apellidos, self.fecha, self.edad, self.aportaciones, self.dir1, self.dir2, self.telf1, 
					self.telf2, self.email, self.sueldo, self.diasLabor, self.sexo, self.nivelAcad, self.cuentaBamc, self.tipoDisc,
					self.nombreRec, self.telfRec, self.celRec, self.ciudad, self.fname])
				QtWidgets.QMessageBox.information(self, 'Informacion', 'Registro Correcto', QtWidgets.QMessageBox.Ok)
			elif self.btnGuardar.text() == 'Modificar':
				if self.selecciona:
						self.guardarImagen()
				else:
					self.fname = self.fotoActual
				modificar = QtWidgets.QMessageBox.question(self, 'Confirmación', '¿Desea modificar los datos de este empleado?', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel) # Mensaje de confirmación
				if modificar == QtWidgets.QMessageBox.Ok: # Si decidimos modificar
					self.cursor.execute("UPDATE empleado SET cedula=%s, nombres=%s, apellidos=%s, fecha_nacimiento=%s, edad=%s,  numero_aportaciones=%s, direccion1=%s,"
						"direccion2=%s, telefono1=%s, telefono2=%s, email=%s, sueldo=%s, dias_laborales=%s, genero=%s, nivel_academico=%s, numero_cuenta_bancaria=%s, tipo_discapacidad=%s,"
						"nombre_recomendado=%s, telefono_recomendado=%s, celular_recomendado=%s, ciudad=%s, foto=%s where empleado_oid=%s",
						#" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", 
						[self.cedula, self.nombres, self.apellidos, self.fecha, self.edad, self.aportaciones, self.dir1, self.dir2, self.telf1, 
						self.telf2, self.email, self.sueldo, self.diasLabor, self.sexo, self.nivelAcad, self.cuentaBamc, self.tipoDisc,
						self.nombreRec, self.telfRec, self.celRec, self.ciudad, self.fname, self.id])
					QtWidgets.QMessageBox.information(self, 'Informacion', 'Los datos han sido actualizados', QtWidgets.QMessageBox.Ok)
			self.con.commit()
			self.cursor.close()
			self.con.close()
			self.borrarCampos()
			self.mostrarEmpleados()
		else:
			QtWidgets.QMessageBox.information(self, 'Informacion', 'Escriba un número de cédula correcto', QtWidgets.QMessageBox.Ok)

	def mostrarEmpleados(self):
		conn_string = "host={0} user={1} dbname={2} password={3}".format(self.host, self.user, self.dbname, self.password)
		self.con = psycopg2.connect(conn_string)
		self.cursor = self.con.cursor()
		self.cursor.execute("SELECT * FROM empleado")
		self.listaEmpleados.clear() # Se vacia la lista
		self.listaEmpleados.setColumnCount(23)
		self.listaEmpleados.setHorizontalHeaderLabels(['Id', 'Cédula', 'Nombres', 'Apellidos', 'Fecha Nacimiento', 
			'Edad', '# Aportaciones', 'Dirección 1', 'Dirección 2', 'Teléfono 1', 'Teléfono 2', 'Email', 'Sueldo', 'Dias Laborales',
			'Género', '	Nivel Académico', '# Cuenta', 'Discapacidad', 'Nombre Recomendado', 'Teléfono Recomendado', 'Celular Recomendado'
			, 'Ciudad', 'Foto'])
		self.cur = self.cursor.fetchall()
		self.listaEmpleados.setRowCount(len(self.cur))
		for i, row in enumerate(self.cur):
			for j, val in enumerate(row):
				self.listaEmpleados.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))

	def eliminarEmpleado(self):
		"""Este metodo nos permite eliminar un registro de estudiantes de la base de datos"""
		conn_string = "host={0} user={1} dbname={2} password={3}".format(self.host, self.user, self.dbname, self.password)
		self.con = psycopg2.connect(conn_string)
		self.cursor = self.con.cursor()
		borrar = QtWidgets.QMessageBox.question(self, 'Confirmación', '¿Desea eliminar este empleado?', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel) # Mensaje de confirmación
		if borrar == QtWidgets.QMessageBox.Ok: # Si decidimos borrar
			self.cursor.execute("delete from empleado where empleado_oid = %s", [self.txtID.text()]) # Se ejecuta la sentencia sql
			QtWidgets.QMessageBox.information(self, 'Información', 'Empleado Eliminado', QtWidgets.QMessageBox.Ok) # Se muestra mensaje
			self.con.commit() # Se realiza un conmit
			self.con.close() # Cerramos la conexion
			self.mostrarEmpleados() # Se actualiza la tabla de clientes
			self.btnEliminar.setEnabled(False)
			self.borrarCampos() # Se eliminan los campos del formulario


	def buscarEmpleado(self): # Metodos de busqueda por id y por correo
		conn_string = "host={0} user={1} dbname={2} password={3}".format(self.host, self.user, self.dbname, self.password)
		self.con = psycopg2.connect(conn_string)
		self.cursor = self.con.cursor()
		item = self.cbxBusq.currentText() # Se guarda en variable el combobox de busqueda
		self.dato = self.txtBusq.text() # Guarda en variable el dato a buscar
		if self.dato == "" or self.dato.isspace():  # Si no se ingresa nada se muestran todos los datos 
			self.mostrarEmpleados()
		else:
			if item == 'Cédula':
				self.cursor.execute("SELECT * FROM empleado where cedula = %s", [self.dato])
			elif item == 'Apellidos':
				self.cursor.execute("SELECT * FROM empleado where apellidos = %s", [self.dato])
			elif item == 'Nombres':
				self.cursor.execute("SELECT * FROM empleado where nombres = %s", [self.dato])
			elif item == 'Ciudad':
				self.cursor.execute("SELECT * FROM empleado where ciudad = %s", [self.dato])
			
			self.listaEmpleados.clear() # Se vacia la lista
			self.listaEmpleados.setColumnCount(23)
			self.listaEmpleados.setHorizontalHeaderLabels(['Id', 'Cédula', 'Nombres', 'Apellidos', 'Fecha Nacimiento', 
				'Edad', '# Aportaciones', 'Dirección 1', 'Dirección 2', 'Teléfono 1', 'Teléfono 2', 'Email', 'Sueldo', 'Dias Laborales',
				'Género', '	Nivel Académico', '# Cuenta', 'Discapacidad', 'Nombre Recomendado', 'Teléfono Recomendado', 'Celular Recomendado'
				, 'Ciudad', 'Foto'])
			self.cur = self.cursor.fetchall()
			self.listaEmpleados.setRowCount(len(self.cur))
			for i, row in enumerate(self.cur):
				for j, val in enumerate(row):
					self.listaEmpleados.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))


	def seleccionarFila(self):
		"""Este metodo nos permite seleccionar una fila de la tabla y obtener sus datos"""
		datos = self.listaEmpleados.selectedItems()
		self.txtID.setText(datos[0].text())
		self.txtCedula.setText(datos[1].text())
		self.txtNombres.setText(datos[2].text())
		self.txtApellidos.setText(datos[3].text())
		self.txtFecha.setDate(datetime.datetime.strptime(datos[4].text(), "%d/%m/%Y"))
		self.txtEdad.setValue(int(datos[5].text()))
		self.txtAport.setValue(int(datos[6].text()))
		self.txtDireccion1.setText(datos[7].text())
		self.txtDireccion2.setText(datos[8].text())
		self.txtTelefono1.setText(datos[9].text())
		self.txtTelefono2.setText(datos[10].text())
		self.txtCorreo.setText(datos[11].text())
		self.txtSueldo.setValue(float(datos[12].text()))
		self.txtDias.setValue(int(datos[13].text()))
		index1 = self.cbxSexo.findText(datos[14].text(), QtCore.Qt.MatchFixedString)
		if index1 >= 0:
			self.cbxSexo.setCurrentIndex(index1)
		index2 = self.cbxNivel.findText(datos[15].text(), QtCore.Qt.MatchFixedString)
		if index2 >= 0:
			self.cbxNivel.setCurrentIndex(index2)
		self.txtCuenta.setText(datos[16].text())
		index3 = self.cbxDiscapacidad.findText(datos[17].text(), QtCore.Qt.MatchFixedString)
		if index3 >= 0:
			self.cbxDiscapacidad.setCurrentIndex(index3)
		self.txtNombreRecom.setText(datos[18].text())
		self.txtTelefonoRecom.setText(datos[19].text())
		self.txtCelularRecom.setText(datos[20].text())
		self.txtCiudad.setText(datos[21].text())
		self.verImagen.setPixmap(QtGui.QPixmap(str(datos[22].text())))
		self.btnEliminar.setEnabled(True)
		self.btnGuardar.setText("Modificar")
		self.fotoActual = str(datos[22].text())

	def borrarCampos(self):
		"""Este metodo nos permite vaciar los campos del formulario de registro"""
		self.txtID.setText("")
		self.txtCedula.setText("")
		self.txtNombres.setText("")
		self.txtApellidos.setText("")
		self.txtEdad.setValue(1)
		self.txtAport.setValue(0)
		self.txtDireccion1.setText("")
		self.txtDireccion2.setText("")
		self.txtTelefono1.setText("")
		self.txtTelefono2.setText("")
		self.txtCorreo.setText("")
		self.txtSueldo.setValue(float(0))
		self.txtDias.setValue(0)
		self.cbxSexo.setCurrentIndex(0)
		self.cbxNivel.setCurrentIndex(0)
		self.txtCuenta.setText("")
		self.cbxDiscapacidad.setCurrentIndex(0)
		self.txtNombreRecom.setText("")
		self.txtTelefonoRecom.setText("")
		self.txtCelularRecom.setText("")
		self.txtCiudad.setText("")

		self.btnEliminar.setEnabled(False)
		self.verImagen.setPixmap(QtGui.QPixmap(''))
		self.btnGuardar.setText("Guardar")

	def buscarImagen(self):
		"""Este metodo nos permite buscar una imagen en nuestro equipo"""
		fname, filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', 'C:\\', 'Image Files (*.jpg)')
		if fname:
			self.selecciona = True
			self.cargarImagen(fname)
		else:
			print('Imagen inválida')
			self.selecciona = False

	def cargarImagen(self, fname):
		"""Este metodo nos permite cargar la imagen seleccionada
			fname representa al nombre del archivo
		"""
		self.image = cv2.imread(fname, cv2.IMREAD_COLOR)
		self.mostrarImagen()

	def mostrarImagen(self):
		"""Este metodo nos permite mostrar en la aplicacion la imagen seleccionada"""
		qformat = QtGui.QImage.Format_Indexed8
		if len(self.image.shape) == 3: # rows[0], cols[1], channels[2]
			if (self.image.shape[2]) == 4:
				qformat = QtGui.QImage.Format_RGB8888
			else:
				qformat = QtGui.QImage.Format_RGB888
		img = QtGui.QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0], qformat)
		img = img.rgbSwapped()
		self.verImagen.setPixmap(QtGui.QPixmap.fromImage(img))

	def guardarImagen(self):
		"""Este metodo nos permite guardar la imagen en nuestro equipo"""
		self.random = randint(0, 999999999999)
		self.fname = "./fotos/img_"+str(self.random)+'.jpg'
		cv2.imwrite(self.fname, self.image)
		print(self.fname)

	def verificar(self, nro):
		self.mensaje = ''
		l = len(nro)
		if l == 10 or l == 13: # verificar la longitud correcta
			cp = int(nro[0:2])
			if cp >= 1 and cp <= 22: # verificar codigo de provincia
				tercer_dig = int(nro[2])
				if tercer_dig >= 0 and tercer_dig < 6 : # numeros enter 0 y 6
					if l == 10:
						return self.validar_ced_ruc(nro,0)     
					elif l == 13:
						return self.validar_ced_ruc(nro,0) and nro[10:13] != '000' # se verifica q los ultimos numeros no sean 000
				elif tercer_dig == 6:
					return self.validar_ced_ruc(nro,1) # sociedades publicas
				elif tercer_dig == 9: # si es ruc
					return self.validar_ced_ruc(nro,2) # sociedades privadas
				else:
					return False
			else:
				return False
		else:
			return False

	def validar_ced_ruc(self, nro, tipo):
		total = 0
		if tipo == 0: # cedula y r.u.c persona natural
			base = 10
			d_ver = int(nro[9])# digito verificador
			multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
		elif tipo == 1: # r.u.c. publicos
			base = 11
			d_ver = int(nro[8])
			multip = (3, 2, 7, 6, 5, 4, 3, 2 )
		elif tipo == 2: # r.u.c. juridicos y extranjeros sin cedula
			base = 11
			d_ver = int(nro[9])
			multip = (4, 3, 2, 7, 6, 5, 4, 3, 2)
		for i in range(0,len(multip)):
			p = int(nro[i]) * multip[i]
			if tipo == 0:
				total+=p if p < 10 else int(str(p)[0])+int(str(p)[1])
			else:
				total+=p
		mod = total % base
		val = base - mod if mod != 0 else 0
		return val == d_ver


class MyProxyStyle(QtWidgets.QProxyStyle):
	""" Soporte para pantallas 4k"""
	pass
	def pixelMetric(self, QStyle_PixelMetric, option=None, widget=None):

		if QStyle_PixelMetric == QtWidgets.QStyle.PM_SmallIconSize:
			return 40
		else:
			return QtWidgets.QProxyStyle.pixelMetric(self, QStyle_PixelMetric, option, widget)


if __name__ == "__main__":
	app =  QtWidgets.QApplication(sys.argv)
	#app.setStyle(QtWidgets.QStyleFactory.create('Fusion')) # <- Choose the style
	myStyle = MyProxyStyle('Fusion')    # The proxy style should be based on an existing style,
	# like 'Windows', 'Motif', 'Plastique', 'Fusion', ...
	app.setStyle(myStyle)
	#dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
	#app.setStyleSheet(dark_stylesheet)
	window = Estudiante()
	window.show()
	sys.exit(app.exec_())




