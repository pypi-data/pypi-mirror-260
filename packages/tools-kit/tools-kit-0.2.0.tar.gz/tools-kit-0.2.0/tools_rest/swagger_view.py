from drf_yasg import openapi
from rest_framework import serializers

def map_field_type(field, serializerMethodField = None):
    if(type(field) == serializers.SerializerMethodField) and serializerMethodField:
        (isList, model) = serializerMethodField[field.field_name]
        openapi_result = openapi.Schema(type=openapi.TYPE_OBJECT, properties={field.name: map_field_type(field._field) for field in model()})
        if isList:
            openapi_result = openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi_result)
        return openapi_result
    
    field_mapping = {
        serializers.CharField: openapi.TYPE_STRING,
        str: openapi.TYPE_STRING,
        
        serializers.IntegerField: openapi.TYPE_INTEGER,
        int: openapi.TYPE_INTEGER,
        
        serializers.BooleanField: openapi.TYPE_BOOLEAN,
        bool: openapi.TYPE_BOOLEAN,
        
        serializers.SerializerMethodField: openapi.TYPE_OBJECT
        # Adicione mais mapeamentos conforme necessário para outros tipos de campos
    }
    mapped_field = field_mapping.get(type(field), openapi.TYPE_STRING)
    return openapi.Schema(type=mapped_field)

class SwaggerResultViewModel:
    def __init__(self, obj, list = False, methodField = None):
        if hasattr(obj, 'fields'):  # Verifica se é um serializador
            openapi_result = openapi.Schema(type=openapi.TYPE_OBJECT, properties={field.name: map_field_type(field._field, methodField) for field in obj()})
            if list:
                openapi_result = openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi_result)
        else:
            properties = map_field_type(obj)
            openapi_result = openapi.Schema(type=properties)
        
        self.openapi = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'result': openapi_result,
                'errors': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            }
        )