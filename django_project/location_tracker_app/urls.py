from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .user_ops.views import UserViewSet
from .location_ops.views import LocationViewSet
router = DefaultRouter(trailing_slash=False)
router.register('users', UserViewSet, base_name='users')
router.register('locations', LocationViewSet, base_name='locations')
urlpatterns = router.urls
