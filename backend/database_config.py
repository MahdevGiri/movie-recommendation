import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConfig:
    """
    Database configuration and connection management for PostgreSQL.
    
    This class handles:
    - Database connection setup
    - Environment variable loading
    - Connection pooling
    - Session management
    """
    
    def __init__(self):
        """Initialize database configuration."""
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '5432')
        self.database = os.getenv('DB_NAME', 'movie_recommendation')
        self.username = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD', 'password')
        
        # Create database URL
        self.database_url = f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        
        # Create SQLAlchemy engine
        self.engine = create_engine(
            self.database_url,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            echo=False  # Set to True for SQL query logging
        )
        
        # Create session factory
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Create base class for models
        self.Base = declarative_base()
    
    def get_session(self):
        """
        Get a database session.
        
        Returns:
            SQLAlchemy session object
        """
        return self.SessionLocal()
    
    def test_connection(self):
        """
        Test the database connection.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def create_tables(self):
        """
        Create all tables defined in the models.
        """
        try:
            self.Base.metadata.create_all(bind=self.engine)
            print("✅ Database tables created successfully")
        except Exception as e:
            print(f"❌ Failed to create tables: {e}")
    
    def drop_tables(self):
        """
        Drop all tables (use with caution!).
        """
        try:
            self.Base.metadata.drop_all(bind=self.engine)
            print("✅ Database tables dropped successfully")
        except Exception as e:
            print(f"❌ Failed to drop tables: {e}")

# Global database configuration instance
db_config = DatabaseConfig() 