from typing import ClassVar
from starlette_admin.contrib.sqla import ModelView


class UserAdminView(ModelView):
    fields: ClassVar[list[str]] = [
        "id",
        "email",
        "is_active",
        "is_admin",
        "role",
        "joined_at",
    ]
    exclude_fields_from_create: ClassVar[list[str]] = ["joined_at"]
    exclude_fields_from_edit: ClassVar[list[str]] = ["joined_at"]
    exclude_fields_from_list: ClassVar[list[str]] = ["joined_at"]

    # Qidiruv va filter
    searchable_fields: ClassVar[list[str]] = ["email"]
    filters: ClassVar[list[str]] = ["is_active", "is_admin", "role"]

    export_fields: ClassVar[list[str]] = [
        "id",
        "email",
        "is_active",
        "is_admin",
        "role",
        "joined_at",
    ]
    export_types: ClassVar[list[str]] = ["csv", "excel", "pdf", "print"]


class ArticleAdminView(ModelView):
    fields: ClassVar[list[str]] = [
        "id",
        "title",
        "content",
        "published",
        "created_at",
        "updated_at",
        "author",
    ]
    exclude_fields_from_create: ClassVar[list[str]] = ["created_at", "updated_at"]
    exclude_fields_from_edit: ClassVar[list[str]] = ["created_at", "updated_at"]
    exclude_fields_from_list: ClassVar[list[str]] = ["content"]

    # Qidiruv va filter
    searchable_fields: ClassVar[list[str]] = ["title", "content"]
    filters: ClassVar[list[str]] = ["published"]

    export_fields: ClassVar[list[str]] = [
        "id",
        "title",
        "content",
        "published",
        "created_at",
        "updated_at",
        "author",
    ]
    export_types: ClassVar[list[str]] = ["csv", "excel", "pdf", "print"]
