from api.tests.conftest import client


def test_tables_get(client):
    route = "/tables"

    response = client.get(path=route)

    assert response.get_json()[0] == {"anzahlPlaetze": 4, "tischnummer": 1}

    assert response.status_code == 200


def test_tables_free(client):
    route = "/tables/free"
    payload = {
        "start_time": "2023-10-17--15:30:00",
        "end_time": "2023-10-17--16:30:00"
    }

    response = client.get(path=route, query_string=payload)

    assert response.get_json() == [2, 4, 5, 6]

    assert response.status_code == 200


def test_tables_free_invalid_time(client):
    route = "/tables/free"
    payload = {
        "start_time": "2023-10-17--00:60:00"
    }

    response = client.get(path=route, query_string=payload)

    assert response.status_code != 200

