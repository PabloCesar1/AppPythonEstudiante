import psycopg2 # Descargado
from PyQt5 import QtWidgets #importamos QtWidgets desde el modulo PyQt5

# Información de la base de datos
host = 'localhost'
user = 'admin'
dbname = 'DB_Empleados'
password = 'userDB'

# Cadena de conexión
def conexionDB(self):
	try:
		conn_string = "host={0} user={1} dbname={2} password={3}".format(host, user, dbname, password)
		con = psycopg2.connect(conn_string)
		print("Conexión establecida")
		con.close() # si da error eliminar
	except Exception as e:
		QtWidgets.QMessageBox.information(self, 'Información', 'Error al conectarse a la base de datos', QtWidgets.QMessageBox.Ok)


#cursor = con.cursor()
#cursor.execute("DROP TABLE IF EXISTS empleado;")
#print("Finished dropping table (if existed)")

#cursor.execute("CREATE TABLE empleado (id serial, cedula text NOT NULL);")

# Insert some data into table
#cursor.execute("INSERT INTO empleado (cedula) VALUES (%s);", ['1236'])
#cursor.execute("INSERT INTO empleado (cedula) VALUES (%s);", ['654'])
#cursor.execute("INSERT INTO empleado (cedula) VALUES (%s);", ['545'])
#cursor.execute("INSERT INTO empleado (cedula) VALUES (%s);", ['3333333333'])


#con.commit()
#cursor.close()
#con.close()
