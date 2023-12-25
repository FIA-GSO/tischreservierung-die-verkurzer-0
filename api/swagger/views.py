from flask import redirect
from flask_swagger_ui import get_swaggerui_blueprint

from api.swagger import swagger_blueprint


def init_swagger_routes(app):
    swagger_url = '/swagger'
    api_url = '/swagger/static/swagger.yaml'
    swagger_ui_blueprint = get_swaggerui_blueprint(
        swagger_url,
        api_url,
        config={  # Swagger UI config overrides
            'app_name': "Tisch Reservierung"
        }
    )

    @app.route('/')
    def index():
        return redirect(swagger_url, code=302)

    app.register_blueprint(swagger_ui_blueprint, url_prefix=swagger_url)
    app.register_blueprint(swagger_blueprint)
