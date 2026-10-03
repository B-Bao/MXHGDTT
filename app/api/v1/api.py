from fastapi import APIRouter
from app.api.v1.endpoints import reports, courses, learning, tests
from app.api.v1.endpoints.system import lives, news, notifications, admin_gifts
api_router = APIRouter()
api_router.include_router(reports.router)
api_router.include_router(courses.router)
api_router.include_router(learning.router)
api_router.include_router(tests.router)
api_router.include_router(lives.router)
api_router.include_router(news.router)
api_router.include_router(notifications.router)
api_router.include_router(admin_gifts.router)
