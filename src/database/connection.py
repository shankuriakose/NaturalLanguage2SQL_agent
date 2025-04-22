from typing import Optional
from langchain_community.utilities import SQLDatabase
from src.config.settings import get_settings
from src.utils.logger import logger

class DatabaseConnection:
    _instance: Optional[SQLDatabase] = None
    
    @classmethod
    def get_connection(cls) -> SQLDatabase:
        """Get a database connection instance"""
        if cls._instance is None:
            logger.info("Initializing new database connection")
            try:
                settings = get_settings()
                cls._instance = SQLDatabase.from_uri(
                    settings.DATABASE_URI,
                    include_tables=settings.INCLUDE_TABLES,
                    sample_rows_in_table_info=settings.SAMPLE_ROWS
                )
                logger.info(f"Database connection established successfully to {settings.DATABASE_URI}")
                
                # Log available tables
                tables = cls._instance.get_usable_table_names()
                logger.info(f"Available tables in database: {', '.join(tables)}")
                
            except Exception as e:
                logger.error(f"Failed to establish database connection: {str(e)}", exc_info=True)
                raise
        return cls._instance
    
    @classmethod
    def close_connection(cls):
        """Close the database connection if it exists"""
        if cls._instance is not None:
            try:
                # Note: SQLDatabase from langchain doesn't have a direct close method
                # The underlying engine connection pool handles connection lifecycle
                cls._instance = None
                logger.info("Database connection cleared")
            except Exception as e:
                logger.error(f"Error while closing database connection: {str(e)}", exc_info=True)
                raise

if __name__ == "__main__":
    try:
        db = DatabaseConnection.get_connection()
        logger.info(f"Tables in DB: {db.get_usable_table_names()}")
    except Exception as e:
        logger.error(f"Test failed: {e}")
    finally:
        DatabaseConnection.close_connection()