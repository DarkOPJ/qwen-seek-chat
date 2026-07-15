from app.core.repository import AsyncSQLBaseRepository
from app.models import ResourceModel


class AsyncResourceRepository(AsyncSQLBaseRepository):
    model = ResourceModel
    object_name = "resource"
