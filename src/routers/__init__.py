from src.routers.incident import api_router as incident_router

__all__ = [
    "list_of_routes",
]

list_of_routes = [
    incident_router,
]
