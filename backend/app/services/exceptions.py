class ServiceError(Exception):
    """Базовое исключение сервисного слоя."""


class NotFoundError(ServiceError):
    """Ресурс не найден."""


class ConflictError(ServiceError):
    """Конфликт данных (например, дубликат)."""
