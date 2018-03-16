from django.urls import path, re_path, include
from rest_framework import renderers
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view
from . import views

api_view = get_swagger_view(title='workflow API')

router = DefaultRouter()
router.register(r'process', views.ProcessViewSet)

urlpatterns = [
    re_path(r'^api/', include(router.urls)),

]
