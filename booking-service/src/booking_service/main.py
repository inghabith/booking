from fastapi import FastAPI

from booking_service.presentation.api.error_handlers import register_error_handlers
from booking_service.presentation.api.routers.booking_router import router as booking_router


def create_app() -> FastAPI:
    app = FastAPI(title="booking-service", version="0.1.0")
    register_error_handlers(app)
    app.include_router(booking_router)

    @app.get("/health", tags=["health"])
    def health():
        return {"status": "ok", "service": "booking-service"}

    return app


app = create_app()
