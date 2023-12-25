from api.tests.conftest import client


def test_swagger(client):
    route = "/swagger"
    response = client.get(path=route, follow_redirects=True)

    assert response.status_code == 200
    assert "swagger-ui" in response.get_data(as_text=True)
    assert "errors-wrapper" not in response.get_data(as_text=True)


def test_swagger_index(client):
    route = "/"
    response = client.get(path=route, follow_redirects=True)

    assert response.status_code == 200
    assert "swagger-ui" in response.get_data(as_text=True)
    assert "errors-wrapper" not in response.get_data(as_text=True)


def test_swagger_static_file(client):
    static_file = 'swagger.yaml'
    route = f"/swagger/static/{static_file}"

    response = client.get(route)

    assert response.status_code == 200
