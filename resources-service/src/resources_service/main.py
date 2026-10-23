from fastapi import FastAPI

from resources_service.presentation.api.error_handlers import register_error_handlers
from resources_service.presentation.api.routers.resource_router import (
    router as resource_router,
)


def create_app() -> FastAPI:
    app = FastAPI(title="resources-service", version="0.1.0")
    register_error_handlers(app)
    app.include_router(resource_router)

    @app.get("/health", tags=["health"])
    def health():
        return {"status": "ok", "service": "resources-service"}

    return app


app = create_app()
