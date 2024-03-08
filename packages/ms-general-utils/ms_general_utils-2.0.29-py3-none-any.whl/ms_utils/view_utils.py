"""
View Utils
"""
import json
from datetime import datetime

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from ms_utils import prepare_json_response, PaginationSchema, abort_bad_request, abort_not_found
from flask import current_app, request, g
from sqlalchemy import inspect
from sqlalchemy import or_

from .model_utils import generic_get_serialize_data
from .validation_utils import validate_generic_form


def has_column(model, column_name):
    return column_name in [c.key for c in inspect(model).columns]


class DataDecoder(json.JSONDecoder):
    def decode(self, obj):
        boolean_text = ['true', 'false', 'True', 'False']
        data = super().decode(obj)
        for d in data.keys():
            if data[d] in boolean_text:
                data[d] = eval(data[d].capitalize())
        return data


class ViewGeneralMethods:
    """
    View generic Methods
    """
    ma = None
    db = None
    model = None
    schema = None
    instance = None
    item_pk = 'object_id'
    columns_filter_icontains = []
    key_kwarg_filter_icointains = 'q'

    def get_db(self):
        """
        Get SQLAlchemy instance
        """
        if self.db is not None:
            return self.db
        if 'db' in current_app.config.keys() and isinstance(current_app.config.get('db'), SQLAlchemy):
            return current_app.config.get('db')
        raise ValueError("'SQLAlchemy' is not defined.")

    def get_ma(self):
        """
        Get Marshmallow instance
        """
        if self.ma is not None:
            return self.ma
        if 'ma' in current_app.config.keys() and isinstance(current_app.config.get('ma'), Marshmallow):
            self.ma = current_app.config.get('ma')
            return current_app.config.get('ma')
        raise ValueError("'Marshmallow' is not defined.")

    def get_queryset(self):
        """
        Get query
        """
        if self.model is None:
            raise ValueError("'Model' is not defined.")
        return self.model.query

    def get_filter_icontains(self, queryset, **kwargs):
        if self.key_kwarg_filter_icointains in kwargs.keys() and len(self.columns_filter_icontains) > 0:
            conditions = []
            for column in self.columns_filter_icontains:
                conditions.append(getattr(self.model, column).ilike(f"%{kwargs['q']}%"))
            queryset = queryset.filter(or_(*conditions))
        return queryset

    def get_filter(self, **kwargs):
        queryset = self.get_queryset()
        user_data = g.get('user')
        if request.args.get('authenticated_user_only') and user_data:
            if has_column(self.model, 'user_id'):
                queryset = queryset.filter_by(user_id=user_data['id'])
            else:
                queryset = queryset.filter_by(employee_id=user_data['id'])
        columns = inspect(self.model).column_attrs.keys()
        for f in kwargs.keys():
            if f in columns:
                queryset = queryset.filter_by(**json.loads(json.dumps({f: kwargs.get(f)}), cls=DataDecoder))
        queryset = self.get_filter_icontains(queryset, **kwargs)
        return queryset

    def get_item(self, pk):
        self.instance = self.get_queryset().filter_by(id=pk).first()
        if not self.instance:
            return abort_not_found()
        return self.instance

    def get_list_without_pagination(self, **kwargs):
        """
        List items without pagination
        :return: json
        """
        queryset = self.get_filter(**kwargs)
        return generic_get_serialize_data(self.schema(many=True), queryset)

    def get_list_with_pagination(self, **kwargs):
        """
        List items with pagination
        :param: kwargs
        :return: json
        """
        page = int(request.args.get('page')) if request.args.get('page') else 1
        per_page = int(request.args.get('per_page')) if request.args.get('per_page') else 10
        queryset = self.get_filter(**kwargs)
        queryset = queryset.paginate(page=page, per_page=per_page)
        queryset.items = generic_get_serialize_data(self.schema(many=True), queryset.items)
        return generic_get_serialize_data(
            PaginationSchema(self.schema(many=True)).pagination_sub_class, queryset)

    def list(self, **kwargs):
        """
        Generic list
        :return: jsonify
        """
        if request.args.get('not_paginate'):
            data = self.get_list_without_pagination(**{**kwargs, **request.args})
        else:
            data = self.get_list_with_pagination(**{**kwargs, **request.args})

        return prepare_json_response(f'{self.model.__name__} get successfully', data=data)

    @staticmethod
    def prepare_data_form():
        if request.is_json:
            return request.json
        return json.loads(json.dumps(dict(request.form)), cls=DataDecoder)

    def get_context(self, **kwargs):
        context = {**kwargs}
        if self.item_pk is not None and self.item_pk in request.view_args:
            self.get_item(request.view_args.get(self.item_pk))
            context['instance'] = self.instance
        return context

    def validate(self, validation_class, data):
        validate_generic_form(validation_class(context=self.get_context()), data)

    def update_or_create(self, validation_class, object_id=None):
        """
        Generic method for create or update provider
        :param validation_class:
        :param object_id:
        :return: jsonify
        """
        data = self.prepare_data_form()
        action_text = 'created'
        self.validate(validation_class, data)

        try:
            if object_id is None:
                self.create(data)
            else:
                action_text = 'updated'
                self.update(data)
            self.get_db().session.commit()
        except ValueError:
            self.get_db().session.rollback()
            abort_bad_request(f'{self.model.__name__} can not be {action_text} successfully')
        return prepare_json_response(f'{self.model.__name__} {action_text} successfully')

    def create(self, data):
        """
        Generic Create method
        :param data:
        :return:
        """
        if self.model is None:
            raise ValueError("'Model' is not defined.")
        self.instance = self.model(**data)
        self.get_db().session.add(self.instance)
        return self.instance

    def update(self, data):
        """
        Generic Update method
        :param data:
        :return:
        """
        for key, value in data.items():
            if hasattr(self.instance, key):
                attribute = getattr(self.instance, key)
                if not hasattr(attribute, '__tablename__'):
                    # If the attribute is not a relationship
                    setattr(self.instance, key, value)

        if hasattr(self.instance, 'updated_at') and 'updated_at' not in data.keys():
            setattr(self.instance, 'updated_at', datetime.now())

    def details(self, object_id):
        """
        Generic details method
        :param object_id:
        :return:
        """
        self.get_item(object_id)
        return prepare_json_response(f'{self.model.__name__} get successfully',
                                     data=generic_get_serialize_data(self.schema(), self.instance))

    def delete(self, object_id):
        """
        Generic delete method
        :param object_id:
        :return:
        """
        self.get_queryset().filter_by(id=object_id).delete()
        self.get_db().session.commit()
        return prepare_json_response(f'{self.model.__name__} deleted successfully!')

    def generic_change_boolean(self, object_id, field):
        """
        Generic change boolean method
        :param object_id:
        :param field:
        :return:
        """
        model_object = self.get_db().get_or_404(self.model, object_id)
        self.model.query.filter_by(id=object_id).update({field: not getattr(model_object, field)})
        self.get_db().session.commit()
        return prepare_json_response(
            f'{self.model.__name__} field {field} updated to {getattr(model_object, field)} successfully!')
