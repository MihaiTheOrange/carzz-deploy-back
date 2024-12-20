from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()


# SUPA_KEY = os.getenv('SUPA_KEY')
# SUPA_URL = os.getenv('SUPA_URL')
# BUCKET_NAME = os.getenv('BUCKET_NAME')
# BUCKET_PROF_PIC = os.getenv('BUCKET_PROF_PIC')

SUPA_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJmamN0a3V5dnpneGtyd3VzY3h2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAyMDI4NjIsImV4cCI6MjA0NTc3ODg2Mn0.ES5q_xvrWwmfPbCkurGrR8WMlSjgoBH0CYvqTDSpyUs'
SUPA_URL = 'https://bfjctkuyvzgxkrwuscxv.supabase.co'
BUCKET_NAME = 'announcement_images'
BUCKET_PROF_PIC = 'profile_pics'

supabase: Client = create_client(SUPA_URL, SUPA_KEY)
