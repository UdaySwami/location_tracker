from rest_framework.viewsets import ModelViewSet

from .serializer import LocationSerializer
from ..models import Location
from ..response import Response


class LocationViewSet(ModelViewSet):
    http_method_names = ('get', 'post')
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    model = Location

    def retrieve(self, request, *args, **kwargs):
        return Response().with_data(LocationSerializer(self.get_object()).data)

    def list(self, request, *args, **kwargs):
        location = Location.objects.all()
        return Response().with_data(LocationSerializer(location, many=True).data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'user': request.user}, many=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response().with_data(LocationSerializer(instance, many=True).data)

    def get_permissions(self):
        permissions = super().get_permissions()
        # permissions.append(UserPermissions())
        return permissions
