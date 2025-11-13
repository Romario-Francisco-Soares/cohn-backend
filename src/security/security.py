from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# ----------------------------------------------------------------------
# 🔧 Configurações globais
# ----------------------------------------------------------------------
ALLOWED_ORIGINS = [
    "https://cohn.netlify.app",
    "https://www.cohn.netlify.app",
    "https://cohn-backend.vercel.app"
]


# ----------------------------------------------------------------------
# 🏗️ Criação da aplicação
# ----------------------------------------------------------------------
def create_app() -> FastAPI:
    app = FastAPI()

    # ✅ Middleware CORS configurado corretamente
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "Accept"],
    )

    # ------------------------------------------------------------------
    # 🧱 Middleware de segurança (não sobrescreve CORS)
    # ------------------------------------------------------------------
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)

        # Define apenas se ainda não existir — para não anular CORS
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault(
            "Content-Security-Policy",
            (
                "frame-ancestors 'none'; "
                "script-src 'self' https://cohn.netlify.app; "
                "img-src 'self' data:; "
                "font-src 'self'; "
                "connect-src 'self' https://cohn.netlify.app; "
                "base-uri 'self'; "
                "form-action 'self'; "
            ),
        )
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault(
            "Strict-Transport-Security", "max-age=31536000; includeSubDomains"
        )
        response.headers.setdefault(
            "Permissions-Policy", "geolocation=(), camera=(), microphone=(), fullscreen=(self)"
        )

        return response

    # ------------------------------------------------------------------
    # 🧩 Handler para requisições OPTIONS (preflight)
    # ------------------------------------------------------------------
    @app.options("/{rest_of_path:path}")
    async def preflight_handler(request: Request):
        origin = request.headers.get("origin")
        response = JSONResponse({"status": "ok"})
        if origin in ALLOWED_ORIGINS:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, Accept"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        return response

    # ------------------------------------------------------------------
    # ⚠️ Tratamento global de exceções
    # ------------------------------------------------------------------
    @app.exception_handler(Exception)
    async def all_exceptions_handler(request: Request, exc: Exception):
        origin = request.headers.get("origin")
        response = JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
        )
        if origin in ALLOWED_ORIGINS:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

    return app


# ----------------------------------------------------------------------
# 🍪 Função de definição de cookies JWT seguros
# ----------------------------------------------------------------------
def setting_cookies(response: JSONResponse, token: str):
    """
    Define cookies HTTP-only com o token JWT.
    """
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=1800,  # 30 minutos
        path="/",
    )
    return response
