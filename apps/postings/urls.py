from django.urls import path, include

from rest_framework import routers

from apps.postings.views import PostingViewSet

router = routers.DefaultRouter()
router.register('', PostingViewSet, basename='postings')

urlpatterns = [
    path('', include(router.urls)),
]
