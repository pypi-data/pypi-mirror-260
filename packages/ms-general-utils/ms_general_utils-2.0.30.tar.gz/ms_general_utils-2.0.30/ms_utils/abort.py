from flask import abort, jsonify, make_response


def abort_response(data, code):
    """
    Generic abort response
    """
    abort(make_response(jsonify(data), code))


def abort_unauthorized(sms='UNAUTHORIZED', **kwargs):
    """
    Abort unauthorized
    """
    abort_response({
        "message": sms,
        **kwargs
    }, 401)


def abort_forbidden(sms='FORBIDDEN', **kwargs):
    """
    Abort forbidden
    """
    abort_response({
        "message": sms,
        **kwargs
    }, 403)


def abort_not_found(sms='NOT FOUND', **kwargs):
    """
    Abort not found
    """
    abort_response({
        "message": sms,
        **kwargs
    }, 404)


def abort_bad_request(sms='BAD REQUEST', **kwargs):
    """
    Abort bad request
    """
    abort_response({
        "message": sms,
        **kwargs
    }, 400)


def abort_validation(sms='VALIDATION ERROR', **kwargs):
    """
    Abort Validation
    """
    abort_response({
        "message": sms,
        **kwargs
    }, 422)
