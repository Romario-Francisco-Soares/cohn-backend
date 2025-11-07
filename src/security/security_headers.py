from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

def create_app():
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # ou "https://cohn.netlify.app"
        allow_credentials=True,
        allow_methods=["*"], # ou ["GET", "POST", "OPTIONS"]
        allow_headers=["*"], # ou ["Authorization", "Content-Type"]
    )

    app.middleware("http")(add_security_headers)

    return app

async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)

    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = (
        "frame-ancestors 'none'; "
        "script-src 'self'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self' https://cohn.netlify.app; "
        "base-uri 'self'; "
        "form-action 'self'; "
    )
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Permissions-Policy"] = (
        "geolocation=(), camera=(), microphone=(), fullscreen=(self)"
    )

    return response
