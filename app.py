"""Aplicación de Registro de Estudiantes
Creado el 25 de Enero de 2018
@author: Pablo España B.
"""

import sys
import os
import sqlite3
import datetime
import cv2
from PyQt5 import uic, QtWidgets, QtGui #importamos uic y QtWidgets desde el modulo PyQt5
from random import randint


qtCreatorFile = "diseño.ui" # Nombre del archivo aquí.
if not os.path.exists('database'):
	os.makedirs('database')
if not os.path.exists('fotos'):
	os.makedirs('fotos')

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile) # usammos loadUiType para cargar el diseño de qt creator

class Estudiante(QtWidgets.QMainWindow, Ui_MainWindow):  # Creamos nuestra clase con sus parametros (QtWidgets.QMainWindow y el diseño de qt creator
	"""Este clase contiene los metodos para el manejo de registro de estudiantes"""
	def __init__(self):             # Metodos init para iniciar la aplicacion
		"""Metodo constructor de la clase"""
		QtWidgets.QMainWindow.__init__(self) # Preparamos una ventana principal
		Ui_MainWindow.__init__(self) # Iniciar el diseño de qt creator
		self.setupUi(self)  # Inicializamos la configuracion de la interfaz
		self.setWindowTitle(u"Gestión de empleados")
		self.image = None
		########## VALIDACIONES DE CAMPOS ##############
		self.soloNumeros = QtGui.QIntValidator()
		self.txtCedula.setValidator(self.soloNumeros)
		self.txtTelefono1.setValidator(self.soloNumeros)
		self.txtTelefono2.setValidator(self.soloNumeros)
		self.txtTelefonoRecom.setValidator(self.soloNumeros)
		self.txtCelularRecom.setValidator(self.soloNumeros)
		###############################################
		self.btnBuscarImg.clicked.connect(self.buscarImagen) # evento producido cuando se selecciona un elemento
		self.btnGuardar.clicked.connect(self.registrarEstudiante) # Id del boton conectado a la funcion guardarCliente
		self.btnBuscar.clicked.connect(self.buscarEstudiante) # Id del boton conectado a la funcion guardarCliente
		self.btnLimpiar.clicked.connect(self.borrarCampos) # Id del boton conectado a la funcion guardarCliente
		self.btnEliminar.clicked.connect(self.eliminarEstudiante) # Id del boton conectado a la funcion guardarCliente
		self.listaEstudiantes.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows) # seleccionar solo filas
		self.listaEstudiantes.setSelectionMode(QtWidgets.QTableWidget.SingleSelection) # usar seleccion simple, una fila a la vez
		self.listaEstudiantes.itemPressed.connect(self.seleccionarFila) # evento producido cuando se selecciona un elemento
		self.btnEliminar.setEnabled(False)
		self.conexionDB() # Al iniciar la aplicacion se crea la base de datos
		self.mostrarEstudiantes()

	def closeEvent(self, event):
		"""Este metodo nos permite confirmar el cierre de una ventana"""
		cerrar = QtWidgets.QMessageBox.question(self, "Salir", "¿Seguro que quieres salir de la aplicación?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
		if cerrar == QtWidgets.QMessageBox.Yes:
			event.accept()
		else: event.ignore()
		
	def conexionDB(self):
		"""Este metodo nos permite la conexion a la base de datos interna"""
		self.con = sqlite3.connect("./database/estudiantes.bd") # Conexion a la base de datos
		self.cursor = self.con.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS estudiante(id INTEGER PRIMARY KEY AUTOINCREMENT, cedula text not null, nombres text not null, apellidos text not null, fecha text not null, telefono text not null, ciudad text not null, nivel text not null, foto text)")
		self.con.commit()

	def registrarEstudiante(self):
		"""Este metodo nos permite registrar y modificar estudiantes en la base de datos"""
		self.con = sqlite3.connect("./database/estudiantes.bd")
		self.cursor = self.con.cursor()
		self.id = self.txtID.text()
		self.cedula = str(self.txtCedula.text())
		self.nombres = str(self.txtNombres.text())
		self.apellidos = str(self.txtApellidos.text())
		self.fecha = str(self.txtFecha.text())
		self.telefono = str(self.txtTelefono.text())
		self.ciudad = str(self.txtCiudad.text())
		self.nivel = str(self.cbxNivel.currentText())

		if self.cedula  == "" or self.cedula.isspace() or self.nombres  == "" or self.nombres.isspace() or self.apellidos  == "" or self.apellidos.isspace() or self.ciudad  == "" or self.ciudad.isspace() or self.telefono  == "" or self.telefono.isspace():
			QtWidgets.QMessageBox.information(self, 'Informacion', 'Debe completar todos los campos', QtWidgets.QMessageBox.Ok)
		else:
			#if self.nombre.istitle() and self.marca.istitle() and self.color.isalpha() and self.talla.isdigit() and self.modelo.istitle():
			if  self.btnGuardar.text() == 'Guardar':
				self.guardarImagen()
				self.datos = (self.cedula, self.nombres, self.apellidos, self.fecha, self.telefono, self.ciudad, self.nivel, self.fname)
				self.cursor.execute("INSERT INTO estudiante (cedula, nombres, apellidos, fecha, telefono, ciudad, nivel, foto) VALUES (?,?,?,?,?,?,?,?)", self.datos)
				QtWidgets.QMessageBox.information(self, 'Informacion', 'Registro Correcto', QtWidgets.QMessageBox.Ok)
				self.borrarCampos()
			elif self.btnGuardar.text() == 'Modificar':
				modificar = QtWidgets.QMessageBox.question(self, 'Confirmación', '¿Desea modificar los datos de este estudiante?', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel) # Mensaje de confirmación
				if modificar == QtWidgets.QMessageBox.Ok: # Si decidimos modificar
					self.guardarImagen()
					self.datos = (self.cedula, self.nombres, self.apellidos, self.fecha, self.telefono, self.ciudad, self.nivel, self.fname, self.id)
					self.cursor.execute("UPDATE estudiante set cedula = ?, nombres = ?, apellidos = ?, fecha = ?, telefono = ?, ciudad = ?, nivel = ?, foto = ? where id = ?", self.datos)
					QtWidgets.QMessageBox.information(self, 'Informacion', 'Los datos han sido actualizados', QtWidgets.QMessageBox.Ok)
					self.borrarCampos()
			#else:
			#   QtWidgets.QMessageBox.information(self, 'Informacion', 'Ingrese valores correctos', QtWidgets.QMessageBox.Ok)

		self.con.commit()
		self.con.close()
		self.mostrarEstudiantes()

	def mostrarEstudiantes(self):
		"""Este metodo nos permite mostrar los estudiantes registrados en la base de datos"""
		self.con = sqlite3.connect("./database/estudiantes.bd")
		self.cursor = self.con.cursor()
		self.cursor.execute("SELECT * FROM estudiante")
		self.listaEstudiantes.clear() # Se vacia la lista
		self.listaEstudiantes.setColumnCount(9)
		self.listaEstudiantes.setHorizontalHeaderLabels(['Id', 'Cédula', 'Nombres', 'Apellidos', 'Fecha Nacimiento', 'Teléfono', 'Ciudad', 'Nivel', 'Foto'])
		self.cur = self.cursor.fetchall()
		self.listaEstudiantes.setRowCount(len(self.cur))
		for i, row in enumerate(self.cur):
			for j, val in enumerate(row):
				self.listaEstudiantes.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))

	def eliminarEstudiante(self):
		"""Este metodo nos permite eliminar un registro de estudiantes de la base de datos"""
		self.con = sqlite3.connect("./database/estudiantes.bd") # Conexion a la base de datos
		self.cursor = self.con.cursor() # Creacion del cursor
		borrar = QtWidgets.QMessageBox.question(self, 'Confirmación', '¿Desea eliminar este estudiante?', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel) # Mensaje de confirmación
		if borrar == QtWidgets.QMessageBox.Ok: # Si decidimos borrar
			self.cursor.execute("delete from estudiante where id = (?)", [self.txtID.text()]) # Se ejecuta la sentencia sql
			QtWidgets.QMessageBox.information(self, 'Informacion', 'Estudiante Eliminado', QtWidgets.QMessageBox.Ok) # Se muestra mensaje
			self.con.commit() # Se realiza un conmit
			self.con.close() # Cerramos la conexion
			self.mostrarEstudiantes() # Se actualiza la tabla de clientes
			self.borrarCampos() # Se eliminan los campos del formulario

	def buscarEstudiante(self): # Metodos de busqueda por id y por correo
		"""Este metodo nos permite buscar un estudiante mediante su cedula, nombres, apellidos o nivel"""
		item = self.cbxBusq.currentText() # Se guarda en variable el combobox de busqueda
		self.dato = self.txtBusq.text() # Guarda en variable el dato a buscar
		self.con = sqlite3.connect("./database/estudiantes.bd") # Nos conectamos a la base de datos
		self.cursor = self.con.cursor() # Se crea el cursor
		if self.dato == "" or self.dato.isspace():  # Si no se ingresa nada se muestran todos los datos 
			self.mostrarEstudiantes()
		else:
			if item == 'Cédula':
				self.cursor.execute("SELECT * FROM estudiante where cedula = (?)", [self.dato])
			elif item == 'Apellidos':
				self.cursor.execute("SELECT * FROM estudiante where apellidos = (?)", [self.dato])
			elif item == 'Nombres':
				self.cursor.execute("SELECT * FROM estudiante where nombres = (?)", [self.dato])
			elif item == 'Nivel':
				self.cursor.execute("SELECT * FROM estudiante where nivel = (?)", [self.dato])
			
			self.listaEstudiantes.clear() # Se vacia la lista
			self.listaEstudiantes.setColumnCount(9)
			self.listaEstudiantes.setHorizontalHeaderLabels(['Id', 'Cédula', 'Nombres', 'Apellidos', 'Fecha Nacimiento', 'Teléfono', 'Ciudad', 'Nivel', 'Foto'])
			self.cur = self.cursor.fetchall()
			self.listaEstudiantes.setRowCount(len(self.cur))
			for i, row in enumerate(self.cur):
				for j, val in enumerate(row):
					self.listaEstudiantes.setItem(i, j, QtWidgets.QTableWidgetItem(str(val)))



	def seleccionarFila(self):
		"""Este metodo nos permite seleccionar una fila de la tabla y obtener sus datos"""
		identificador, cedula, nombres, apellidos, fecha, telefono, ciudad, nivel, foto = self.listaEstudiantes.selectedItems()
		self.txtID.setText(identificador.text())
		self.txtCedula.setText(cedula.text())
		self.txtNombres.setText(nombres.text())
		self.txtApellidos.setText(apellidos.text())
		self.txtFecha.setDate(datetime.datetime.strptime(fecha.text(), "%d/%m/%Y"))
		self.txtTelefono.setText(telefono.text())
		self.txtCiudad.setText(ciudad.text())
		self.cbxNivel.setCurrentIndex(int(nivel.text()) - 1)
		self.verImagen.setPixmap(QtGui.QPixmap(str(foto.text())))
		self.btnEliminar.setEnabled(True)
		self.btnGuardar.setText("Modificar")



	def borrarCampos(self):
		"""Este metodo nos permite vaciar los campos del formulario de registro"""
		self.txtID.setText("")
		self.txtCedula.setText("")
		self.txtNombres.setText("")
		self.txtApellidos.setText("")
		self.txtTelefono.setText("")
		self.txtCiudad.setText("")
		self.btnEliminar.setEnabled(False)
		self.verImagen.setPixmap(QtGui.QPixmap(''))
		self.btnGuardar.setText("Guardar")

	def buscarImagen(self):
		"""Este metodo nos permite buscar una imagen en nuestro equipo"""
		fname, filter = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', 'C:\\', 'Image Files (*.jpg)')
		if fname:
			self.cargarImagen(fname)
		else:
			print('Imagen inválida')

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
		#fname, filter = QtWidgets.QFileDialog.getSaveFileName(self, 'Open File', 'C:\\', 'Image Files (*.jpg)')
		#print(fname)
		self.random = randint(0, 999999999999)
		self.fname = "./fotos/img_"+str(self.random)+'.jpg'
		cv2.imwrite(self.fname, self.image)
		print(self.fname)
		#C:/Users/Pablo/Desktop/Documentos/2017/aplicaciones python/estudiantes/fotos/pablo.jpg
		#if fname:
		#   cv2.imwrite(fname, self.image)
		#else:
		#   print('Imagen inválida')

if __name__ == "__main__":
	app =  QtWidgets.QApplication(sys.argv)
	window = Estudiante()
	#window.showFullScreen()
	window.show()
	sys.exit(app.exec_())

