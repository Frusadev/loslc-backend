import dotenv
import os


dotenv.load_dotenv()


PORT = os.getenv('PORT')
DB_STRING = os.getenv('DB_STRING')
GOOGLE_APP_PASSWORD = os.getenv("GOOGLE_APP_PASSWORD")
APP_EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
SERVER_URL = os.getenv("SERVER_URL")
FRONTEND_URL = os.getenv("FRONTEND_URL")
