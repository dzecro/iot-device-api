# tests/test_auth.py

def test_register_user(client):
    response = client.post("/auth/register", json={
        "email": "user@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user@example.com"
    assert "hashed_password" not in data


def test_register_duplicate_email(client):
    client.post("/auth/register", json={"email": "dup@test.com", "password": "pass"})
    response = client.post("/auth/register", json={"email": "dup@test.com", "password": "pass"})
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_success(client):
    client.post("/auth/register", json={"email": "login@test.com", "password": "mypassword"})
    response = client.post("/auth/login", data={
        "username": "login@test.com",
        "password": "mypassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/auth/register", json={"email": "test@test.com", "password": "correct"})
    response = client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "wrong"
    })
    assert response.status_code == 401


def test_protected_route_without_token(client):
    response = client.get("/devices")
    assert response.status_code == 401