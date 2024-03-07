import tools_rest.statuscode as statuscode
from rest_framework.response import Response

class ResultViewModel:
    def __init__(self, *errors:str, result = None):
        self.result = result
        self.errors = []
        if len(errors) == 1 and isinstance(errors[0], list):
            self.errors.extend(errors[0])
        else:
            self.errors.extend(errors)
        self.success = not bool(self.errors)
    
    def add_result(self, model):
        self.result = model
        
    def add_errors(self, *msg:str):
        if len(msg) == 1 and isinstance(msg[0], list):
            self.errors.extend(msg[0])
        else:
            self.errors.extend(msg)
        self.success = False
    
def response(resultview : ResultViewModel, status_code: int = None) -> Response:
    if(status_code is None):
        status_code = statuscode.OK if resultview.success else statuscode.BAD_REQUEST
    return Response(resultview.__dict__,status=status_code)
        
def success(model = None) -> Response:
    result_view_model = ResultViewModel(result=model)
    return Response(result_view_model.__dict__)
    
def bad_request(*msg:str) -> Response:
    errors = []
    if len(msg) == 1 and isinstance(msg[0], list):
        errors.extend(msg[0])
    else:
        errors.extend(msg)
    result_view_model = ResultViewModel(errors)
    return Response(result_view_model.__dict__, status=statuscode.BAD_REQUEST)