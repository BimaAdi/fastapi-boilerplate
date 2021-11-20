from typing import Any, Optional, Union

from fastapi.responses import JSONResponse

class Ok():
    def __init__(self, data:Optional[Any]) -> None:
        if data != None:
            self.data = data
        else:
            self.data = ''

class Created():
    def __init__(self, data:Optional[Any]) -> None:
        if data != None:
            self.data = data
        else:
            self.data = ''

class NoContent():

    def __init__(self) -> None:
        self.data = ''

class BadRequest():
    def __init__(self, message:str) -> None:
        self.message = message

class NotFound():
    def __init__(self, message:str) -> None:
        self.message = message

class InternalServerError():
    def __init__(self, error:str) -> None:
        self.error = error
    
def common_response(res:Union[Ok, Created, BadRequest, NotFound, InternalServerError])->JSONResponse:
    if type(res) == Ok:
        return JSONResponse(content=res.data, status_code=200)
    if type(res) == Created:
        return JSONResponse(content=res.data, status_code=201)
    if type(res) == NoContent:
        return JSONResponse(content=res.data, status_code=204)
    if type(res) == BadRequest:
        return JSONResponse(content={'message': res.message}, status_code=400)
    if type(res) == NotFound:
        return JSONResponse(content={'message': res.message}, status_code=404)
    if type(res) == InternalServerError:
        return JSONResponse(content={'error': res.error}, status_code=500)
