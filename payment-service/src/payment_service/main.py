from fastapi import FastAPI

from payment_service.presentation.api.error_handlers import register_error_handlers
from payment_service.presentation.api.routers.payment_router import router as payment_router


def create_app() -> FastAPI:
    app = FastAPI(title="payment-service", version="0.1.0")
    register_error_handlers(app)
    app.include_router(payment_router)

    @app.get("/health", tags=["health"])
    def health():
        return {"status": "ok", "service": "payment-service"}

    return app


app = create_app()
