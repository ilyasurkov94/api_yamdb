from django.urls import path, include
from rest_framework import routers

from .views import UserAdminViewset


router = routers.DefaultRouter()
router.register('', UserAdminViewset, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
