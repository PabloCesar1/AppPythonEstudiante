"""Aplicación de Registro de Estudiantes
Creado el 25 de Enero de 2018
@author: Pablo España B.
"""

import sys
import os
import sqlite3
import datetime
import cv2 # Descargado opencv-python
from PyQt5 import uic, QtWidgets, QtGui #importamos uic y QtWidgets desde el modulo PyQt5
from random import randint
import psycopg2 # Descargado


qtCreatorFile = "diseño.ui"
if not os.path.exists('database'): os.makedirs('database')
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
		self.btnGuardar.clicked.connect(self.registrarEmpleado) # Id del boton conectado a la funcion guardarCliente
		#self.btnBuscar.clicked.connect(self.buscarEstudiante) # Id del boton conectado a la funcion guardarCliente
		#self.btnLimpiar.clicked.connect(self.borrarCampos) # Id del boton conectado a la funcion guardarCliente
		#self.btnEliminar.clicked.connect(self.eliminarEstudiante) # Id del boton conectado a la funcion guardarCliente
		#self.listaEstudiantes.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows) # seleccionar solo filas
		#self.listaEstudiantes.setSelectionMode(QtWidgets.QTableWidget.SingleSelection) # usar seleccion simple, una fila a la vez
		#self.listaEstudiantes.itemPressed.connect(self.seleccionarFila) # evento producido cuando se selecciona un elemento
		#self.btnEliminar.setEnabled(False)
		 # Conexión a la base de datos creada en postgres
		self.conexionDB()
		#self.mostrarEstudiantes()
			
	def conexionDB(self):
		conn_string = "host={0} user={1} dbname={2} password={3}".format('localhost', 'postgres', 'DB_Empleados', 'anlecap17')
		self.con = psycopg2.connect(conn_string)
		print("Conexión establecida")
		self.cursor = self.con.cursor()
		#self.cursor.execute("INSERT INTO empleado (cedula) VALUES (%s);", [434])
		#self.con.commit()
		#self.cursor.close()
		self.con.close()

	def registrarEmpleado(self):
		conn_string = "host={0} user={1} dbname={2} password={3}".format('localhost', 'postgres', 'DB_Empleados', '123456')
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
		self.sueldo = self.txtSueldo.text()
		self.diasLabor = self.txtDias.text()
		self.sexo = str(self.cbxSexo.currentText())
		self.nivelAcad = str(self.cbxNivel.currentText())
		self.cuentaBamc = str(self.txtCuenta.text())
		self.tipoDisc = str(self.cbxDiscapacidad.currentText())
		self.nombreRec = str(self.txtNombreRecom.text())
		self.telfRec = str(self.txtTelefonoRecom.text())
		self.celRec = str(self.txtCelularRecom.text())
		self.ciudad = str(self.txtCiudad.text())
		if  self.btnGuardar.text() == 'Guardar':
			self.guardarImagen()
			self.verificar()
			self.cursor.execute("INSERT INTO empleado (cedula, nombres, apellidos, fecha_nacimiento, numero_aportaciones, direccion1,"
				"direccion2, telefono1, telefono2, email, sueldo, dias_laborales, genero, nivel_academico, numero_cuenta_bancaria, tipo_discapacidad,"
				"nombre_recomendado, telefono_recomendado, celular_recomendado, ciudad, foto)"
				" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", 
				[self.cedula, self.nombres, self.apellidos, self.fecha, self.aportaciones, self.dir1, self.dir2, self.telf1, 
				self.telf2, self.email, self.sueldo, self.diasLabor, self.sexo, self.nivelAcad, self.cuentaBamc, self.tipoDisc,
				self.nombreRec, self.telfRec, self.celRec, self.ciudad, self.fname])
			self.con.commit()
			self.cursor.close()
			self.con.close()


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
		self.random = randint(0, 999999999999)
		self.fname = "./fotos/img_"+str(self.random)+'.jpg'
		cv2.imwrite(self.fname, self.image)
		print(self.fname)



if __name__ == "__main__":
	app =  QtWidgets.QApplication(sys.argv)
	window = Estudiante()
	#window.showFullScreen()
	window.show()
	sys.exit(app.exec_())

#Validar cédula, revisar
def verificar(cedula):
    l = len(cedula)
    if l == 10 or l == 13: # verificar la longitud correcta
        cp = int(cedula[0:2])
        if cp >= 1 and cp <= 22: # verificar codigo de provincia
            tercer_dig = int(cedula[2])
            if tercer_dig >= 0 and tercer_dig < 6 : # numeros enter 0 y 6
                if l == 10:
                    return __validar_ced_ruc(cedula,0)                       
                elif l == 13:
                    return __validar_ced_ruc(cedula,0) and cedula[10:13] != '000' # se verifica q los ultimos numeros no sean 000
            elif tercer_dig == 6:
                return __validar_ced_ruc(cedula,1) # sociedades publicas
            elif tercer_dig == 9: # si es ruc
                return __validar_ced_ruc(cedula,2) # sociedades privadas
            else:
                raise Exception(u'Tercer digito invalido') 
        else:
            raise Exception(u'Codigo de provincia incorrecto') 
    else:
        raise Exception(u'Longitud incorrecta del numero ingresado')

def __validar_ced_ruc(cedula,tipo):
    total = 0
    if tipo == 0: # cedula y r.u.c persona natural
        base = 10
        d_ver = int(cedula[9])# digito verificador
        multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
    elif tipo == 1: # r.u.c. publicos
        base = 11
        d_ver = int(cedula[8])
        multip = (3, 2, 7, 6, 5, 4, 3, 2 )
    elif tipo == 2: # r.u.c. juridicos y extranjeros sin cedula
        base = 11
        d_ver = int(cedula[9])
        multip = (4, 3, 2, 7, 6, 5, 4, 3, 2)
    for i in range(0,len(multip)):
        p = int(cedula[i]) * multip[i]
        if tipo == 0:
            total+=p if p < 10 else int(str(p)[0])+int(str(p)[1])
        else:
            total+=p
    mod = total % base
    val = base - mod if mod != 0 else 0
    return val == d_ver