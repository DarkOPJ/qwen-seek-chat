from app.core.repository import SQLBaseRepository
from app.models import ResourceModel


class SyncResourceRepository(SQLBaseRepository):
    model = ResourceModel
    object_name = "resource"
