from pymongo import MongoClient

client = MongoClient("localhost:27017")

db = client["carlos"]
collection = db["animales"]

result = collection.insert_one({"name": "gato", "age": 10})
print(f"Documento insertado con _id: {result.inserted_id}")


print("Documentos en 'animales':")
for documento in collection.find():
    print(documento)