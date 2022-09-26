from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.postings.models import Posting
from apps.postings.serializers import PostingListSerializer, PostingCreateSerializer, PostingDetailSerializer


class PostingViewSet(viewsets.ModelViewSet):
    queryset = Posting.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PostingListSerializer
        if self.action == "create":
            return PostingCreateSerializer
        if self.action == "retrieve":
            return PostingDetailSerializer
        return PostingListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)
