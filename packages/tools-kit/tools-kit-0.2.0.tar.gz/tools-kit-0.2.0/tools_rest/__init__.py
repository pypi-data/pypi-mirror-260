from django.conf import settings, urls
from tools_rest.exceptions import exception_400, exception_403, exception_404, exception_500

if hasattr(settings, 'CUSTOM_EXCEPTION'):
    if settings.CUSTOM_EXCEPTION.get('ADD_CUSTOM_HANDLER', False):
        settings.REST_FRAMEWORK['EXCEPTION_HANDLER'] = 'tools_rest.exceptions.exception_handler'
    
    from tools_rest.constants_exc import HTTP_400, HTTP_403, HTTP_404, HTTP_500
    
    custom_ex =settings.CUSTOM_EXCEPTION.get('EXCEPTIONS', {})
    HTTP_400 = custom_ex.get('HTTP_403', HTTP_400)
    HTTP_403 = custom_ex.get('HTTP_403', HTTP_403)
    HTTP_404 = custom_ex.get('HTTP_404', HTTP_404)
    HTTP_500 = custom_ex.get('HTTP_500', HTTP_500)
    
    custom_ex = settings.CUSTOM_EXCEPTION.get('URLS_HANDLER', {})
    if custom_ex.__contains__(400): urls.handler400 = exception_400
    if custom_ex.__contains__(403): urls.handler403 = exception_403
    if custom_ex.__contains__(404): urls.handler404 = exception_404
    if custom_ex.__contains__(500): urls.handler500 = exception_500