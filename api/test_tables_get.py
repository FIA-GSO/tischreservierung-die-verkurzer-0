from conftest import testing_app


def test_tables_get(testing_app):
    route = "/tables"

    response = testing_app.get(path=route)

    assert response.get_json()[0] == {"Plaetze": 4, "Tisch": 1}

    assert response.status_code == 200

    print(response)

