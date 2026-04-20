import os #Permite leer variables de entorno como la que tenemos en el fichero .env
import certifi #Permite verificar la conexión segura con MongoDB Atlas utilizando un certificado de autoridad (CA) confiable.

from pymongo import MongoClient #MongoClient es la clase principal de PyMongo que se utiliza para conectarse a una instancia de MongoDB.
from dotenv import load_dotenv #Su trabajo es leer el fichero .env y cargar las variables de entorno definidas en el entorno de ejecución de Python.

ca = certifi.where() #Devuelve la ubicación del archivo de certificados de autoridad (CA) confiables que se utilizan para verificar la conexión segura con MongoDB Atlas.

load_dotenv() #Basicamente abre el fichero .env y lee el contenido, cargando las variables de definidas en él para que puedan ser accedidas a través de os.getenv().

MONGO_URI= os.getenv("MONGO_URI") #Aquí se utiliza os.getenv() para obtener el valor de la variable "MONGO_URI"
client = MongoClient(MONGO_URI, tlsCAFile=ca)#Crea unna instancia de MongoClient y se la asigna a la variable "client"

for db in client.list_database_names(): #Recorre la lista de nombres de las bases de datos que tenemos en el cluster
    print(db) #Imprime el nombre de cada base de datos.