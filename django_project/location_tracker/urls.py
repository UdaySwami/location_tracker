"""location_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

api_doc_schema_view = get_schema_view(
   openapi.Info(
       title='LCT REST APIs', default_version='v1',
       description='REST API specification for LCT application'), public=True, permission_classes=(),
)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^docs/$', api_doc_schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    url(r'^lct_app/v1/', include('location_tracker_app.urls'))
]
