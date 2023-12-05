from conftest import testing_app


def test_tables_get(testing_app):
    route = "/tables/free"
    payload = {
        "start_time": "2023-10-17--15:30:00",
        "end_time": "2023-10-17--16:30:00"
    }

    response = testing_app.get(path=route, query_string=payload)

    assert response.get_json() == [2, 4, 5, 6]

    assert response.status_code == 200

    print(response)
