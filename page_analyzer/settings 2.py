import dotenv
import os
from urllib.parse import urlparse


env_path = os.path.join(os.path.dirname(__file__), '.env')
dotenv.load_dotenv()
parsed_url = urlparse(os.environ.get('DATABASE_URL'))


DB_HOST = parsed_url.hostname
DB_PORT = parsed_url.port
DB_NAME = parsed_url.path[1::]
DB_USER = parsed_url.username
DB_PASS = parsed_url.password
