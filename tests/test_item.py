from fastapi.testclient import TestClient

def test_find_all(client_fixture: TestClient):
    response = client_fixture.get("/items")
    assert response.status_code == 200 # status_codeが200であることを検証する
    items = response.json()
    assert len(items) == 2 # 取得した検索結果の長さを検証


def test_get_by_id正常系(client_fixture: TestClient):
    response = client_fixture.get("/items/1")
    assert response.status_code == 200
    find_item = response.json()
    assert find_item.get('id') == 1


def test_get_by_id異常系(client_fixture: TestClient):
    response = client_fixture.get("/items/10")
    assert response.status_code == 404
    assert response.json()["detail"] == "item not found"

def find_by_name正常系(client_fixture: TestClient):
    response = client_fixture.get('items/?name=PC')
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2

def find_by_name異常系(client_fixture: TestClient):
    response = client_fixture.get('/items/hoge')
    assert response.status_code == 404
    assert response.json()['detail'] == "item not found"


def test_create(client_fixture: TestClient):
    response = client_fixture.post("/items/create", json={"name": "スマホ", "price": 30000, "user_id": 1})
    assert response.status_code == 201
    item = response.json()
    assert item["id"] == 3
    assert item["name"] == "スマホ"
    assert item["price"] == 30000
    assert item["user_id"] == 1

    response = client_fixture.get("/items")
    assert len(response.json()) == 3


def test_update(client_fixture: TestClient):
    response = client_fixture.put("/items/update/1", json={"name": "PC1UPDATE", "price": 100001, "user_id": 1})
    assert response.status_code == 200
    item = response.json()
    assert item["id"] == 1
    assert item["name"] == "PC1UPDATE"
    assert item["price"] == 100001


def test_update異常系(client_fixture: TestClient):
    response = client_fixture.put("/items/update/10", json={"name": "PC1UPDATE", "price": 100001, "user_id": 1})
    assert response.status_code == 404
    assert response.json()["detail"] == "item not updated"    


def test_delete(client_fixture: TestClient):
    response = client_fixture.delete('/items/delete/1')
    assert response.status_code == 200
    item = response.json()
    assert item["id"] == 1
    assert item["name"] == "PC1"

    response = client_fixture.get("/items")
    assert len(response.json()) == 1
    items = response.json()
    assert items[0]["id"] == 2


def test_delete異常系(client_fixture: TestClient):
    response = client_fixture.delete('/items/delete/10')
    assert response.status_code == 404
    assert response.json()["detail"] == "item not deleted"