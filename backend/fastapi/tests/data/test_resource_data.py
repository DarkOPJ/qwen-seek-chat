class ResourceTestData:
    @property
    def existing_resource(self):
        return {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "name": "resource",
            "status": "active",
        }

    @property
    def add_resource(self):
        return {"name": "new resource", "status": "pending"}

    @property
    def update_resource(self):
        return {"status": "failed"}
