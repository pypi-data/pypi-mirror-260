from flask import current_app
from .requests_utils import request_get


def get_file(obj, f_key):
    """
    Get file from ms data file
    """
    obj_file = getattr(obj, f_key)
    try:
        if obj_file is None:
            return None
        url = f"{current_app.config.get('DATA_FILE_MS_URL')}/{current_app.config.get('DATA_FILE_MS_API')}/{obj_file}"
        response = request_get(url)
        if response.status_code == 200:
            response = response.json()
            return f"{current_app.config.get('DATA_FILE_MS_URL')}{response['data']['path']}"
    except Exception:
        pass
    return None
