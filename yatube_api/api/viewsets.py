from rest_framework import mixins, viewsets


class CreateListViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """Базовый вьюсет только для создания и получения списка."""
