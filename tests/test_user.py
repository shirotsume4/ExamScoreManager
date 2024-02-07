from starlette.testclient import TestClient

from controller.main import app, get_db

client = TestClient(app)
from relpath import add_import_path

add_import_path("../")  # ここで、importしたいツールの場所を相対参照で指定


def temp_db(f):
    def func(SessionLocal, *args, **kwargs):
        # テスト用のDBに接続するためのsessionmaker instanse
        #  (SessionLocal) をfixtureから受け取る

        def override_get_db():
            try:
                db = SessionLocal()
                yield db
            finally:
                db.close()

        # fixtureから受け取るSessionLocalを使うようにget_dbを強制的に変更
        app.dependency_overrides[get_db] = override_get_db
        # Run tests
        f(*args, **kwargs)
        # get_dbを元に戻す
        app.dependency_overrides[get_db] = get_db

    return func


@temp_db
def test_create_user():
    response = client.post("/users/", json={"username": "foo", "password": "fo"})
    assert response.status_code == 200

    response = client.post("/users/", json={"username": "foo", "password": "fo"})
    assert response.status_code == 400


@temp_db
def test_get_all_user():
    client.post("/users/", json={"username": "alice", "password": "abcdef"})
    response = client.get("/users/")
    assert len(response.json()) == 1
    client.post("/users/", json={"username": "bob", "password": "ghijkl"})
    response = client.get("/users/")
    assert len(response.json()) == 2


@temp_db
def test_get_user_by_id():
    client.post("/users/", json={"username": "alice", "password": "abcdef"})
    client.post("/users/", json={"username": "bob", "password": "ghijkl"})
    response = client.get("/users/1")
    assert response.json()["username"] == "alice"
    response = client.get("/users/2")
    assert response.json()["username"] == "bob"
