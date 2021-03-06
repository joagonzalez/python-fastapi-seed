from re import compile
from jwt import decode
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader

from src.config import settings
from src.services.authentication import AuthenticationService


jwt_auth_scheme = APIKeyHeader(name='Authorization')


def decodeToken(token: str):
    '''
        decodeToken: Decodes current verified token with the secret key and HS256 algorithm
    '''
    try:
        payload = decode(token, settings['JWT']['SECRET_KEY'], algorithms='HS256')
    except:
        return None
    return payload


def auth_jwt(token: str = Depends(jwt_auth_scheme), authService: AuthenticationService = Depends()) -> dict:
    '''
        auth_jwt: Request middleware that verifies the Authorization
        key on the header to be compliance with JWT token
    '''
    isValid = compile('^(?s:Bearer).*$')

    if isValid.match(token) is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    tokenString = token.replace('Bearer ', '')

    payload = decodeToken(token=tokenString)
    if not payload or 'id' not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not authService.userExist(payload['id']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return payload


def SecurityRole(roleList: List[str] = []):
    '''
        Security Role: Decorator that verify that the current token
        a valid role to access requested endpoint
    '''
    def check(payload: dict = Depends(auth_jwt)):
        if not payload['role'] in roleList:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return True
    return check
