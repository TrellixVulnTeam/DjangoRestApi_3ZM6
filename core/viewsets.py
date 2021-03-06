from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet


class GenericViewSetMixin(GenericViewSet):
    serializer_classes = {}

    @property
    def user(self):
        return self.request.user

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)


class BaseModelViewSet(ModelViewSet):
    pass


class BaseModelReadOnlyViewSet(ReadOnlyModelViewSet):
    pass