"""Aplicación de Registro de Estudiantes
Creado el 25 de Enero de 2018
@author: Pablo España B.
"""


from PyQt5 import uic, QtWidgets, QtGui, QtCore #importamos uic y QtWidgets desde el modulo PyQt5
import sys



qtCreatorFile = "menu.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile) # usammos loadUiType para cargar el diseño de qt creator

class Estudiante(QtWidgets.QMainWindow, Ui_MainWindow):  # Creamos nuestra clase con sus parametros (QtWidgets.QMainWindow y el diseño de qt creator
	"""Este clase contiene los metodos para el manejo de registro de estudiantes"""
	def __init__(self):             # Metodos init para iniciar la aplicacion
		"""Metodo constructor de la clase"""
		QtWidgets.QMainWindow.__init__(self) # Preparamos una ventana principal
		Ui_MainWindow.__init__(self) # Iniciar el diseño de qt creator
		self.setupUi(self)  # Inicializamos la configuracion de la interfaz
		self.setWindowTitle(u"Menú lateral")


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




