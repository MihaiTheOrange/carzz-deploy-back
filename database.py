from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

YOUR = "Sanitarium0113,:"
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres.bfjctkuyvzgxkrwuscxv:{YOUR}@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
