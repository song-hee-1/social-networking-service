from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination

from apps.postings.models import Posting
from apps.postings.serializers import PostingListSerializer, PostingCreateSerializer, PostingDetailSerializer


class PostingSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostingViewSet(viewsets.ModelViewSet):
    pagination_class = PostingSetPagination

    def get_queryset(self):
        queryset = Posting.objects.prefetch_related('hashtag').all()
        search_condition = self.request.GET.get('search', None)
        hashtag_condition = self.request.GET.get('hashtags', None)
        ordering = self.request.GET.get('ordering', '-create_time')

        try:
            q = Q()

            if search_condition:
                q.add(Q(title__contains=search_condition), q.AND)

            if hashtag_condition:
                q_hashtag = Q()
                for tag in hashtag_condition.split(','):
                    q_hashtag.add(Q(hashtag__name=tag), q_hashtag.OR)
                q.add(q_hashtag, q.AND)

            queryset = queryset.filter(q).distinct().order_by(ordering)
            return queryset

        except Exception as e:
            raise APIException(detail=f'에러가 발생하였습니다. {e}')

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
