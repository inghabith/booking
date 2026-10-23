from fastapi import FastAPI

from notification_service.presentation.api.error_handlers import register_error_handlers
from notification_service.presentation.api.routers.notification_router import (
    router as notification_router,
)


def create_app() -> FastAPI:
    app = FastAPI(title="notification-service", version="0.1.0")
    register_error_handlers(app)
    app.include_router(notification_router)

    @app.get("/health", tags=["health"])
    def health():
        return {"status": "ok", "service": "notification-service"}

    return app


app = create_app()
