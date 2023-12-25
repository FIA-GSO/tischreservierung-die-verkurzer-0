from flask import Blueprint, send_from_directory
import os

swagger_blueprint = Blueprint('swagger_blueprint', __name__, url_prefix='/swagger')


@swagger_blueprint.route('/static/<path:filename>')
def swagger_static(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(base_dir, 'static'), filename)
