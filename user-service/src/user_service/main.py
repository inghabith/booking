from fastapi import FastAPI

from user_service.presentation.api.error_handlers import register_error_handlers
from user_service.presentation.api.routers.user_router import router as user_router


def create_app() -> FastAPI:
    app = FastAPI(title="user-service", version="0.1.0")
    register_error_handlers(app)
    app.include_router(user_router)

    @app.get("/health", tags=["health"])
    def health():
        return {"status": "ok", "service": "user-service"}

    return app


app = create_app()
