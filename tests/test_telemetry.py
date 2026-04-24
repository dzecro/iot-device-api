# tests/test_telemetry.py

def _make_device(client, headers):
    return client.post("/devices", json={
        "name": "Sensor",
        "device_type": "temperature"
    }, headers=headers).json()["id"]


def test_add_telemetry(client, auth_headers):
    device_id = _make_device(client, auth_headers)
    response = client.post(f"/devices/{device_id}/telemetry", json={
        "value": 72.5,
        "unit": "celsius"
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["value"] == 72.5
    assert response.json()["unit"] == "celsius"


def test_get_telemetry_list(client, auth_headers):
    device_id = _make_device(client, auth_headers)
    for v in [70.0, 72.5, 75.0]:
        client.post(f"/devices/{device_id}/telemetry", json={
            "value": v, "unit": "celsius"
        }, headers=auth_headers)
    response = client.get(f"/devices/{device_id}/telemetry", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_telemetry_stats(client, auth_headers):
    device_id = _make_device(client, auth_headers)
    for v in [10.0, 20.0, 30.0]:
        client.post(f"/devices/{device_id}/telemetry", json={
            "value": v, "unit": "celsius"
        }, headers=auth_headers)
    response = client.get(f"/devices/{device_id}/telemetry/stats", headers=auth_headers)
    assert response.status_code == 200
    stats = response.json()
    assert stats["count"] == 3
    assert stats["average"] == 20.0
    assert stats["minimum"] == 10.0
    assert stats["maximum"] == 30.0


def test_telemetry_on_nonexistent_device(client, auth_headers):
    response = client.post("/devices/99999/telemetry", json={
        "value": 50.0, "unit": "celsius"
    }, headers=auth_headers)
    assert response.status_code == 404


def test_stats_with_no_readings(client, auth_headers):
    device_id = _make_device(client, auth_headers)
    response = client.get(f"/devices/{device_id}/telemetry/stats", headers=auth_headers)
    assert response.status_code == 404