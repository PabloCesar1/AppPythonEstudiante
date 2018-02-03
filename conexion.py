import psycopg2 # Descargado
from PyQt5 import QtWidgets #importamos QtWidgets desde el modulo PyQt5

# Información de la base de datos
host = 'localhost'
user = 'postgres'
dbname = 'DB_Empleados'
password = 'anlecap17'

# Cadena de conexión
def conexionDB():
	conn_string = "host={0} user={1} dbname={2} password={3}".format(host, user, dbname, password)
	con = psycopg2.connect(conn_string)
	print("Conexión establecida")
	cursor = con.cursor()
	cursor.execute("INSERT INTO empleado (cedula) VALUES (%s);", [434])
	con.commit()
	cursor.close()
	con.close()

conexionDB()

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