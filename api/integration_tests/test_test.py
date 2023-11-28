import integration_tests.conftest

def test_test(testing_app):
    res = testing_app.get('/')
    print(res)
    return True