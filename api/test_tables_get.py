from conftest import testing_app


def test_tables_get(testing_app):
    route = "/tables"
    payload = {
        "time": "?time=2023-10-17-15:30:00",
    }

    response = testing_app.get(path=route, query_string=payload)

    assert response.get_json()[0] == {'Tisch': 1}

    assert response.status_code == 200

    print(response)

