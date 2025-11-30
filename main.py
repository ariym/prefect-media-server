import uvicorn
from fastapi import FastAPI
from prefect.server.api.server import create_app as create_prefect_app

from get_modules import router as custom_router

def create_app() -> FastAPI:
    # Prefect’s built-in API
    prefect_app = create_prefect_app()

    # Add your custom routes
    prefect_app.include_router(custom_router, prefix="/custom")

    return prefect_app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4200)