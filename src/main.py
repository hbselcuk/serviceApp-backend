from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware

from router.restapi_router import router as restapi_router
from modules.auth.utils import VerifyToken

auth = VerifyToken()

def create_app():
    app = FastAPI()
    app.include_router(restapi_router, dependencies=[Security(auth.verify)])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()

@app.get("/api/private")
def private(auth_result: str = Security(auth.verify)):
    """A valid access token is required to access this route"""
    return auth_result


@app.get("/api/private-scoped")
def private_scoped(auth_result: str = Security(auth.verify, scopes=["read:messages"])):
    """A valid access token and an appropriate scope are required to access
    this route
    """
    return auth_result
