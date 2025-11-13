from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

ALLOWED_ORIGINS = ["https://cohn.netlify.app","https://www.cohn.netlify.app",
                    "https://cohn-backend.vercel.app"
                   ]
methods = ["GET", "POST", "OPTIONS"]
headers = ["Authorization", "Content-Type", "Accept"]

def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "Accept"],
    )
    return app

def setting_cookies(response: JSONResponse, token: str):
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=1800,
        path="/",
    )
    return response