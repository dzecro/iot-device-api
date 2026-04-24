# tests/test_devices.py

def test_create_device(client, auth_headers):
    response = client.post("/devices", json={
        "name": "Temp Sensor A1",
        "device_type": "temperature",
        "location": "Zone B"
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Temp Sensor A1"
    assert data["device_type"] == "temperature"
    assert "id" in data


def test_create_device_requires_auth(client):
    response = client.post("/devices", json={
        "name": "No Auth Device",
        "device_type": "voltage"
    })
    assert response.status_code == 401


def test_list_devices(client, auth_headers):
    client.post("/devices", json={"name": "Device 1", "device_type": "temp"}, headers=auth_headers)
    client.post("/devices", json={"name": "Device 2", "device_type": "voltage"}, headers=auth_headers)
    response = client.get("/devices", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_single_device(client, auth_headers):
    create = client.post("/devices", json={
        "name": "My Sensor",
        "device_type": "pressure"
    }, headers=auth_headers)
    device_id = create.json()["id"]
    response = client.get(f"/devices/{device_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "My Sensor"


def test_update_device(client, auth_headers):
    create = client.post("/devices", json={
        "name": "Old Name",
        "device_type": "temp"
    }, headers=auth_headers)
    device_id = create.json()["id"]
    response = client.patch(f"/devices/{device_id}", json={
        "name": "New Name"
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["name"] == "New Name"
    assert response.json()["device_type"] == "temp"  # unchanged


def test_delete_device(client, auth_headers):
    create = client.post("/devices", json={
        "name": "To Delete",
        "device_type": "temp"
    }, headers=auth_headers)
    device_id = create.json()["id"]
    assert client.delete(f"/devices/{device_id}", headers=auth_headers).status_code == 204
    assert client.get(f"/devices/{device_id}", headers=auth_headers).status_code == 404


def test_get_nonexistent_device(client, auth_headers):
    response = client.get("/devices/99999", headers=auth_headers)
    assert response.status_code == 404