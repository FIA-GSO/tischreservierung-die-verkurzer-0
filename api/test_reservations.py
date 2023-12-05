from conftest import testing_app

def test_get_reservations(testing_app):
    #Arrange
    route = "/reservations"

    response = testing_app.get(route)

    assert response.status_code == 200
    assert response.get_json()[0] == {"dauerMin":60,"pin":1331,"reservierungsnummer":1,"storniert":"False","tischnummer":1,"zeitpunkt":"2022-02-02 17:30:00"}

def test_gadd_reservation(testing_app):
    #arrange
    route ="/add_reservation"

    response = testing_app.get(route)

    assert response.status_code == 200
    assert  response.get_json()[0] == {}