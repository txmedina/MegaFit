from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

uri = "mongodb+srv://megafitAdmin:megafit123@megafit.vaeilyn.mongodb.net/?retryWrites=true&w=majority&appName=MegaFit" #need to put this in env file
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.megafit

users_collection = db.users #use "users_collection" when connecting to users collection 
favorites_collection = db.favoriteExercise #use "favorites_collection" when connecting to favorites collection