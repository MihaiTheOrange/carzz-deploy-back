from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

YOUR = "Sanitarium0113,:"
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres.bfjctkuyvzgxkrwuscxv:{YOUR}@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"

# SUPA_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJmamN0a3V5dnpneGtyd3VzY3h2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAyMDI4NjIsImV4cCI6MjA0NTc3ODg2Mn0.ES5q_xvrWwmfPbCkurGrR8WMlSjgoBH0CYvqTDSpyUs"
# SUPA_URL = "https://bfjctkuyvzgxkrwuscxv.supabase.co"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
