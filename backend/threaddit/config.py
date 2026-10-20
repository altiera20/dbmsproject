from dotenv import dotenv_values

_env = dotenv_values()

DATABASE_URI = _env["DATABASE_URI"]
SECRET_KEY = _env["SECRET_KEY"]
CLOUDINARY_NAME = _env["CLOUDINARY_NAME"]
CLOUDINARY_API_KEY = _env["CLOUDINARY_API_KEY"]
CLOUDINARY_API_SECRET = _env["CLOUDINARY_API_SECRET"]
ELASTICSEARCH_URL = _env.get("ELASTICSEARCH_URL", "http://localhost:9200")
ELASTICSEARCH_INDEX = _env.get("ELASTICSEARCH_INDEX", "threaddit")
