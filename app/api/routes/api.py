from fastapi import APIRouter

from app.api.routes import ping
from app.api.routes import projects
from app.api.routes import tickets
from app.api.routes import kanbanboard
from app.api.routes import kanbanstatus


router = APIRouter()

router.include_router(ping.router, prefix="/ping", tags=["ping"])
router.include_router(projects.router, prefix="/projects", tags=["projects"])
router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
router.include_router(kanbanboard.router, prefix="/kanbanboard", tags=["kanbanboard"])
router.include_router(kanbanstatus.router, prefix="/kanbanstatus", tags=["kanbanstatus"])
