import pytest
from relpath import add_import_path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import drop_database
add_import_path("../src")  # ここで、importしたいツールの場所を相対参照で指定
from controller.main import app
from controller.main import Base

TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///test_temp.db"


@pytest.fixture(scope="function")
def SessionLocal():
    # settings of test database
    TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///test_temp.db"
    engine = create_engine(
        TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

    # Create test database and tables
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Run the tests
    yield SessionLocal

    drop_database(TEST_SQLALCHEMY_DATABASE_URL)
