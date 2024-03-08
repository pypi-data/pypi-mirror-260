"""
Validation utils
"""
from marshmallow import Schema, EXCLUDE

from ms_utils import abort_validation


def validate_generic_form(validation_class, body):
    """
    Generic validation form
    :param validation_class: Validation class
    :param body: dict
    :return: jsonfy | abort
    """
    if body is None:
        raise TypeError('Cannot validate an object of type None')
    errors = validation_class.validate(body)
    if errors:
        abort_validation('VALIDATION ERROR', **{'data': {'errors': errors}})


class BaseSchema(Schema):
    class Meta:
        """
        Meta
        """
        unknown = EXCLUDE
