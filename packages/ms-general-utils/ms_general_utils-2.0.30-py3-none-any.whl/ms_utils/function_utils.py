from flask import current_app

from ms_utils import request_get, abort_unauthorized, abort_forbidden


def get_hierarchy_users_list():
    """
    Return a list of users in my hierarchy
    :return:
    """
    try:
        response = request_get(
            f'{current_app.config.get("AUTH_MS_API")}{current_app.config.get("HIERARCHY_PAYLOAD_API")}')
        if not response.status_code == 200:
            abort_unauthorized()
        return response.json()['data'].get('users')
    except Exception as e:
        abort_forbidden('Error al buscar el rol/hierarchy')


def validate_hierarchy_field(value):
    hierarchy_users_list = get_hierarchy_users_list()
    if value not in hierarchy_users_list:
        abort_forbidden("You do not have permission for this request")
