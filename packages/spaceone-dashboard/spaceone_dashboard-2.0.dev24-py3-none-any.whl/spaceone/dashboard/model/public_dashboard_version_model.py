from mongoengine import *

from spaceone.core.model.mongo_model import MongoModel


class PublicDashboardVersion(MongoModel):
    public_dashboard_id = StringField(max_length=40)
    version = IntField()
    layouts = ListField(default=[])
    variables = DictField(default={})
    settings = DictField(default={})
    variables_schema = DictField(default={})
    domain_id = StringField(max_length=40)
    created_at = DateTimeField(auto_now_add=True)

    meta = {
        "updatable_fields": [],
        "minimal_fields": [
            "public_dashboard_id",
            "version",
            "domain_id",
            "created_at",
        ],
        "ordering": ["-version"],
        "indexes": ["public_dashboard_id", "version", "domain_id", "created_at"],
    }
