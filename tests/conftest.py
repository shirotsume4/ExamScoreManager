import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database
from relpath import add_import_path
add_import_path("../")  # ここで、importしたいツールの場所を相対参照で指定
from src.controller.main import Base, get_db, app
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"

@pytest.fixture(scope="function")
def SessionLocal():
    # settings of test database
    TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"
    engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


    # Create test database and tables
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Run the tests
    yield SessionLocal
    
    drop_database(TEST_SQLALCHEMY_DATABASE_URL)
    