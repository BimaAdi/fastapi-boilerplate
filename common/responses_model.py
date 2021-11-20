from pydantic import BaseModel

class NoContent(BaseModel):

    pass

class BadRequest(BaseModel):

    message: str

class NotFound(BaseModel):

    message: str

class InternalServerError(BaseModel):

    error: str
