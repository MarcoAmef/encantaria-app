from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/encantaria")

client = MongoClient(MONGO_URI)
db = client["encantaria"]

usuarios = db["usuarios"]
anuncios = db["anuncios"]
mensagens = db["mensagens"]
