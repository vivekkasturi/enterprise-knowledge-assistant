from fastapi import HTTPException, Request

class AppException(HTTPException):

    def __init__(self, status_code: int, detail: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.status_code = status_code
        self.detail = detail