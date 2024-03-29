from typing import Optional
import requests

import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer

from modules.auth.config import get_settings


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        """Returns HTTP 403"""
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)


class UnauthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication"
        )


class VerifyToken:
    """Does all the token verification using PyJWT"""

    def __init__(self):
        self.config = get_settings()

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f"{self.config.auth0_issuer}/protocol/openid-connect/certs"
        
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    async def verify(
        self,
        security_scopes: SecurityScopes,
        token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer()),
        req: Request = None,
    ):
        if token is None:
            raise UnauthenticatedException

        # This gets the 'kid' from the passed token
        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(
                token.credentials
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            raise UnauthorizedException(str(error))
        except jwt.exceptions.DecodeError as error:
            raise UnauthorizedException(str(error))

        try:
            payload = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=self.config.auth0_algorithms,
                audience=self.config.auth0_api_audience,
                issuer=self.config.auth0_issuer,
            )
        except Exception as error:
            raise UnauthorizedException(str(error))

        if len(security_scopes.scopes) > 0:
            self._check_claims(payload, "scope", security_scopes.scopes)
        userInfoUrl = f"{self.config.auth0_issuer}/protocol/openid-connect/userinfo"
        r = requests.get(userInfoUrl, headers={"Authorization": f"Bearer {token.credentials}"})

        req.userInfo = r.json()
        
        return payload

    def _check_claims(self, payload, claim_name, expected_value):
        if claim_name not in payload:
            raise UnauthorizedException(
                detail=f'No claim "{claim_name}" found in token'
            )

        payload_claim = payload[claim_name]

        if claim_name == "scope":
            payload_claim = payload[claim_name].split(" ")

        for value in expected_value:
            if value not in payload_claim:
                raise UnauthorizedException(detail=f'Missing "{claim_name}" scope')

