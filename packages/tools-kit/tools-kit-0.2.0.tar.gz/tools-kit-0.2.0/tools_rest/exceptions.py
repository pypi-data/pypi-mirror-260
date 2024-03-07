from rest_framework.exceptions import ValidationError
from rest_framework import views
from tools_rest.response_view import ResultViewModel
from django.conf import settings
from django.http import HttpResponseForbidden, Http404, JsonResponse
from tools_rest.statuscode import BAD_REQUEST, FORBIDDEN, NOT_FOUND, INTERNAL_SERVER_ERROR
from tools_rest.constants_exc import HTTP_400, HTTP_403, HTTP_404, HTTP_500

if hasattr(settings, 'CUSTOM_EXCEPTION'):
    custom_ex =settings.CUSTOM_EXCEPTION.get('EXCEPTIONS', {})
    HTTP_400 = custom_ex.get('HTTP_403', HTTP_400)
    HTTP_403 = custom_ex.get('HTTP_403', HTTP_403)
    HTTP_404 = custom_ex.get('HTTP_404', HTTP_404)
    HTTP_500 = custom_ex.get('HTTP_500', HTTP_500)

def exception_handler(exc, context):
    result = ResultViewModel()
    status_code = BAD_REQUEST
    response = views.exception_handler(exc, context)
    
    if isinstance(exc, ValidationError):
        for field, messages in exc.detail.items():
            field = f'{field}: ' if field and field != 'non_field_errors' else ''
            if type(messages) is list:
                msg = messages[0] if messages else None
            else:
                msg = messages
            result.add_errors(f'{field}{msg}')
    elif isinstance(exc, HttpResponseForbidden):
        result.add_errors(HTTP_403)
        status_code = FORBIDDEN
    elif isinstance(exc, Http404):
        result.add_errors(HTTP_404)
        status_code = NOT_FOUND
    elif not settings.DEBUG and response.status_code == INTERNAL_SERVER_ERROR:
        result.add_errors(HTTP_500)
        status_code = INTERNAL_SERVER_ERROR
    else:
        if isinstance(exc.detail, str):
            exc.detail = exc.detail.replace('"', '')
        result.add_errors(exc.detail)
        status_code = response.status_code

    response.data = result.__dict__
    response.status_code = status_code
    return response

def exception_400(request, exception): 
    return json_response_exception(BAD_REQUEST, HTTP_400)

def exception_403(request, exception):
    return json_response_exception(FORBIDDEN, HTTP_403)

def exception_404(request, exception):
    return json_response_exception(NOT_FOUND, HTTP_404)

def exception_500(request, exception): 
    return json_response_exception(INTERNAL_SERVER_ERROR, HTTP_500)

def json_response_exception(statuscode, msg_error) -> JsonResponse:
    result = ResultViewModel(msg_error)
    return JsonResponse(result.__dict__, status=statuscode)