from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

InvalidCredentials = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

NotFound = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Resource not found.",
)
