import uvicorn
from fastapi import FastAPI
from starlette.applications import Starlette
from prefect.server.api.server import create_app as create_prefect_app

from get_modules import router as custom_router

def create_app():
    # Prefect's built-in API
    prefect_app = create_prefect_app()
    
    # Create our custom FastAPI app
    custom_app = FastAPI(title="Custom Routes")
    custom_app.include_router(custom_router, prefix="/custom", tags=["custom"])
    
    # Use ASGI wrapper - this intercepts requests BEFORE Prefect's app
    # and routes custom paths to our app, everything else to Prefect
    class CombinedASGIApp:
        def __init__(self, prefect_app, custom_app):
            self.prefect_app = prefect_app
            self.custom_app = custom_app
        
        async def __call__(self, scope, receive, send):
            # Check the path BEFORE routing to either app
            if scope["type"] == "http":
                path = scope.get("path", "")
                
                # Route custom paths to our app FIRST
                if path.startswith("/custom"):
                    await self.custom_app(scope, receive, send)
                    return
                else:
                    # Everything else goes to Prefect
                    await self.prefect_app(scope, receive, send)
                    return
            else:
                # For non-HTTP (like websockets), route to Prefect
                await self.prefect_app(scope, receive, send)
    
    return CombinedASGIApp(prefect_app, custom_app)


app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4200)
