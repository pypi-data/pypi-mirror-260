from functools import wraps

from flask import g, current_app, request

from ms_utils import abort_bad_request, abort_unauthorized, request_get, abort_forbidden
from ms_utils.function_utils import get_hierarchy_users_list


class NotAuthenticate(object):
    """
    Not Authentication Class
    """

    def dispatch_request(self, **kwargs):
        user = None
        try:
            response = request_get(f'{current_app.config.get("AUTH_MS_API")}/auth/check-authentication')
            if response.status_code == 200:
                user = response.json()['data']
        except Exception:
            pass
        g.setdefault('user', user)
        return super(NotAuthenticate, self).dispatch_request(**kwargs)


class IsAuthenticate(object):
    """
    Is Authenticate Class
    """

    def dispatch_request(self, **kwargs):
        self.validate_authentication()
        return super(IsAuthenticate, self).dispatch_request(**kwargs)

    @staticmethod
    def validate_authentication():
        config = current_app.config
        if not config.get('AUTH_MS_API'):
            abort_bad_request('The authentication API (AUTH_MS_API) is not configured')

        response = request_get(f'{current_app.config.get("AUTH_MS_API")}/auth/check-authentication')
        if not response.status_code == 200:
            abort_unauthorized()
        g.setdefault('user', response.json()['data'])


class HasHierarchy(object):
    """
    Has Hierarchy Class

    Class to verify users has a hierarchy, in that case modify a get_queryset method
    """
    config = None
    hierarchy_field = None
    hierarchy_api = None
    hierarchy_users_list = []

    def handle_init_vars(self):
        # Init vars
        self.config = current_app.config
        self.hierarchy_field = self.config.get('HIERARCHY_PAYLOAD_FIELD')
        self.hierarchy_api = self.config.get('HIERARCHY_PAYLOAD_API')

    def handle_validations(self):
        if not self.hierarchy_field:
            abort_bad_request('The hierarchy field (HIERARCHY_PAYLOAD_FIELD) is not configured')

        if not self.hierarchy_api:
            abort_bad_request('The hierarchy api (HIERARCHY_PAYLOAD_API) is not configured')

        if not self.config.get('AUTH_MS_API'):
            abort_bad_request('The authentication API (AUTH_MS_API) is not configured')

    def get_queryset(self):
        queryset = super(HasHierarchy, self).get_queryset()
        payload_value = request.args.get(self.hierarchy_field)
        if payload_value and payload_value in self.hierarchy_users_list:
            return queryset.filter_by(**{self.hierarchy_field: payload_value})
        self.hierarchy_users_list.append(g.get('user')['id'])
        condition = getattr(self.model, self.hierarchy_field).in_(self.hierarchy_users_list)
        queryset = queryset.filter(condition)
        return queryset

    def dispatch_request(self, **kwargs):
        self.handle_init_vars()

        self.handle_validations()

        self.hierarchy_users_list = get_hierarchy_users_list()

        if self.hierarchy_field in request.args or 'id' in request.view_args:
            payload_value = int(request.args.get(self.hierarchy_field))
            arg_value = request.view_args.get('id')
            if (payload_value in self.hierarchy_users_list or payload_value == g.get('user')['id']
                    or arg_value in self.hierarchy_users_list or arg_value == g.get('user')['id']):
                return super(HasHierarchy, self).dispatch_request(**kwargs)
            abort_forbidden("You do not have permission for this request")

        return super(HasHierarchy, self).dispatch_request(**kwargs)


def validate_permission(permission_required=None, permission_type="api"):
    if permission_required is None:
        abort_forbidden("You do not have permission for this request")

    config = current_app.config
    if not config.get('AUTH_MS_API'):
        abort_bad_request('The authentication API (AUTH_MS_API) is not configured')
    if not config.get('APP_NAME'):
        abort_bad_request('The app name (APP_NAME) is not configured')
    if not (isinstance(permission_required, tuple)
            or isinstance(permission_required, list)
            or isinstance(permission_required, set)
            or isinstance(permission_required, dict)):
        abort_bad_request('The permission_required variable must be iterable')
    response = request_get(f'{current_app.config.get("AUTH_MS_API")}/user-rol-permission/me', params={
        'not_paginate': True,
        'permission_type': permission_type,
        'app': config.get('APP_NAME')
    })
    if not response.status_code == 200:
        abort_unauthorized()
    permissions = response.json()['data']
    if isinstance(permission_required, tuple):
        return validate_tuple(permission_required, permissions)

    if isinstance(permission_required, dict):
        return validate_dict(permission_required, permissions)


def validate_tuple(permission_required, permissions):
    for permission in permission_required:
        if not any(permission == p['permission'] for p in permissions):
            abort_forbidden("You do not have permission for this request")
    return True


def validate_dict(permission_required, permissions):
    permission = permission_required.get(request.method)
    if not any(permission == p['permission'] for p in permissions):
        abort_forbidden("You do not have permission for this request")
    return True


class ApiPermission(object):
    """
    Api Permission Class
    """
    permission_required = None
    permission_type = 'api'

    def dispatch_request(self, **kwargs):
        validate_permission(self.permission_required, self.permission_type)
        return super(ApiPermission, self).dispatch_request(**kwargs)


def view_decorator(func):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            if func():
                return view_func(*args, **kwargs)
            abort_forbidden()

        return _wrapped_view

    return decorator


def permission_decorator(permissions):
    def check_perms():
        perms = permissions
        if isinstance(permissions, str):
            perms = (permissions,)
        return validate_permission(perms)

    return view_decorator(check_perms)


def authentication_decorator():
    def check_authentication():
        auth = IsAuthenticate()
        auth.validate_authentication()
        return True

    return view_decorator(check_authentication)
