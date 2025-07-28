from decouple import Config, RepositoryEnv

config = Config(repository=RepositoryEnv("config/.env"))

MONGO_URI= config("MONGO_URI", default="mongodb://localhost:27017")  
DB_NAME = config("DB_NAME")
COLLECTION_NAME=config("COLLECTION_NAME")
LOGS_COLLECTION=config("LOGS_COLLECTION")