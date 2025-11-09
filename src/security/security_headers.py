from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://cohn.netlify.app",
            "https://www.cohn.netlify.app",
            "https://cohn-backend.vercel.app"
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = (
            "frame-ancestors 'none'; "
            "script-src 'self' https://cohn.netlify.app;  "
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

    @app.exception_handler(Exception)
    async def all_exceptions_handler(request, exc):
        response = JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
        )
        response.headers["Access-Control-Allow-Origin"] = "https://cohn.netlify.app"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

    return app
