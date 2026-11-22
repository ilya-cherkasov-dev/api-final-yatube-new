from rest_framework import permissions


class IsAuthenticatedAuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Читать могут все, создавать авторизованные, менять только автор."""

    def has_object_permission(self, request, view, obj):
        # Проверку авторизации беру у родителя, здесь проверяю автора.
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
