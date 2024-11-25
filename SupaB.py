from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()


SUPA_KEY = os.getenv('SUPA_KEY')
SUPA_URL = os.getenv('SUPA_URL')
BUCKET_NAME = os.getenv('BUCKET_NAME')
BUCKET_PROF_PIC = os.getenv('BUCKET_PROF_PIC')

supabase: Client = create_client(SUPA_URL, SUPA_KEY)
