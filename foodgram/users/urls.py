from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MyUserViewSet

app_name = 'users'

v1_router = DefaultRouter()

v1_router.register('users', MyUserViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
