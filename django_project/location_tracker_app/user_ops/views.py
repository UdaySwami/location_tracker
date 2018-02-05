from django.contrib.auth.hashers import check_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import list_route, detail_route
from rest_framework.viewsets import ModelViewSet

from .permissions import UserPermissions
from .serializer import UserSerializer, LoginRequestSerializer, UserTrackSerializer, AllUserTrackSerializer
from ..exceptions import InvalidCredentials, InvalidAPIRequest
from ..models import User, Location
from ..response import Response
from ..utils import get_distance_covered


class UserViewSet(ModelViewSet):
    http_method_names = ('get', 'post')
    queryset = User.objects.all()
    serializer_class = UserSerializer
    model = User

    @list_route(methods=['post'], authentication_classes=[], permission_classes=[])
    def signup(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response().with_data(self.serializer_class(instance).data)

    @swagger_auto_schema(request_body=LoginRequestSerializer)
    @list_route(methods=['post'], authentication_classes=[], permission_classes=[])
    def login(self, request):
        try:
            login_request = LoginRequestSerializer(data=request.data)
            login_request.is_valid(raise_exception=True)
            user = self.model.objects.get_user_by_email(email=login_request.data['email'])
            if not check_password(login_request.data['password'], user.password):
                raise InvalidCredentials()
            return Response().with_data(UserSerializer(user).data)
        except User.DoesNotExist:
            return Response(InvalidCredentials()).get_response()
        except Exception as e:
            return Response(e).get_response()

    @detail_route(methods=['get'])
    def tracks(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        locations = Location.objects.filter(user=User.objects.get(id=self.kwargs['pk'])).filter(is_first=True)
        if start_date:
            locations = locations.filter(time__gte=start_date)
        if end_date:
            locations = locations.filter(time__lte=end_date)
        data = UserTrackSerializer(locations, many=True).data
        return Response().with_data(data)

    @list_route(methods=['get'])
    def locations(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        locations = Location.objects.filter().filter(is_first=True)
        if start_date:
            locations = locations.filter(time__gte=start_date)
        if end_date:
            locations = locations.filter(time__lte=end_date)
        data = AllUserTrackSerializer(locations, many=True).data
        return Response().with_data(data)

    def retrieve(self, request, *args, **kwargs):
        if self.kwargs['pk'] == 'me':
            return Response().with_data(UserSerializer(request.user).data)
        else:
            return Response().with_data(UserSerializer(self.get_object()).data)

    def list(self, request, *args, **kwargs):
        users = User.objects.all()
        return Response().with_data(UserSerializer(users, many=True).data)

    def create(self, request, *args, **kwargs):
        raise InvalidAPIRequest()

    def get_permissions(self):
        permissions = super().get_permissions()
        permissions.append(UserPermissions())
        return permissions
