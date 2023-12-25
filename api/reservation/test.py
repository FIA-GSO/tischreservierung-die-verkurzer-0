from api.tests.conftest import client


def test_get_reservations(client):
    # Arrange
    route = "/reservations"
    # Act
    response = client.get(path=route)
    # Assert
    assert response.status_code == 200
    assert response.get_json()[0] == {"dauerMin": 60, "pin": 1331, "reservierungsnummer": 1, "storniert": "False",
                                      "tischnummer": 1, "zeitpunkt": "2022-02-02 17:30:00"}


def test_add_reservations(client):
    # Arrange
    route = "/reservations"
    payload = {
        "table_number": 2,
        "duration_minutes": 0,
        "pin": 6901,
        "reservation_number": 7,
        "timestamp": "2023-12-13 14:16:55"
    }
    # Act
    response = client.post(path=route, json=payload)
    # Assert
    assert response.status_code == 201


def test_add_reservations_Incorrect_Value(client):
    route = "/reservations"
    payload = {
        "table": 2,
        "duration": 0,
        "pin": 6901,
        "reservation": 7,
        "timestamp": "2023-12-13 144:16:55"
    }

    response = client.post(path=route, json=payload)

    assert response.status_code == 400


def test_patch_reservations(client):
    # Arrange
    route = "/reservations"
    payload = {
        "table_number": 3,
        "duration_minutes": 20,
        "pin": 1336,
        "reservation_number": 6,
        "timestamp": "2022-02-02 20:30:00",
    }

    # Act
    response = client.patch(path=route, json=payload)

    # Assert
    assert response.status_code == 200
