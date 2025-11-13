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
        allow_methods=methods,
        allow_headers=headers,
    )
    return app

def setting_cookies(response: JSONResponse, token: str, cookie_name: str):
    response.set_cookie(
        key=cookie_name,
        value=token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=1800,
        path="/",
    )
    return response