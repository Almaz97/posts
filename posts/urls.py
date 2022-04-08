from django.urls import path, include
from rest_framework import routers
from .views import PostViewSet

router = routers.SimpleRouter()

router.register('posts', PostViewSet, 'posts')

urlpatterns = [
    path('v1/', include(router.urls)),
]
