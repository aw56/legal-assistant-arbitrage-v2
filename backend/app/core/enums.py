from enum import Enum


class UserRole(str, Enum):
    """Единый Enum для ролей пользователей"""

    admin = "admin"
    lawyer = "lawyer"
    user = "user"
    client = "client"


__all__ = ["UserRole"]
