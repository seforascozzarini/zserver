from django.db.models import Q

from .exceptions import HTTPException


def get_boolean_param(request, param_name, field_name=None, required=False):
    param = request.query_params.get(param_name, None)
    if param is not None:
        if param == 'true':
            return True
        elif param == 'false':
            return False
        else:
            raise HTTPException(400, {param_name: 'invalid'})
    elif required:
        raise HTTPException(400, {param_name: 'required'})
    return param


def filterby_boolean_param(qs, request, param_name, field_name=None, required=False):
    field_name = field_name or param_name
    param = get_boolean_param(request, param_name, required)
    if param is not None:
        return qs.filter(**{field_name: param})
    return qs


def list_or_filter(request, param_name, field_name=None, required=False):
    field_name = field_name or param_name
    values = request.query_params.getlist(param_name, [])
    if len(values) == 0:
        if required:
            raise HTTPException(400, {param_name: 'required'})
        else:
            return None
    filters = Q()
    for value in values:
        filters |= Q(**{field_name: value})
    return filters


def filterby_or_list_param(qs, request, param_name, field_name=None, required=False):
    field_name = field_name or param_name
    filters = list_or_filter(request, param_name, field_name, required)
    if filters:
        return qs.filter(filters)
    return qs