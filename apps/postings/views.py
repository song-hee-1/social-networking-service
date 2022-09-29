import datetime

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action

from apps.postings.models import Posting, Like
from apps.postings.serializers import PostingListSerializer, PostingCreateSerializer, PostingDetailSerializer, \
    PostingLikeSerializer, PostingRestoreSerializer
from apps.postings.permissions import AuthorAndStaffAllEditOrReadOnly


class PostingSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostingViewSet(viewsets.ModelViewSet):

    permission_classes = [AuthorAndStaffAllEditOrReadOnly]

    pagination_class = PostingSetPagination

    def get_queryset(self):
        queryset = Posting.objects.prefetch_related('hashtag').all().filter(is_delete=0)
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
        return PostingDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=pk)

        # 상세보기시 단순 조회수 증가
        # instance.hits += 1
        # instance.save()

        # 쿠키를 이용한 중복 조회수 방지 : 매일 자정에 쿠기 초기화
        tomorrow = datetime.datetime.replace(timezone.datetime.now(), hour=23, minute=59, second=0)
        expires = datetime.datetime.strftime(tomorrow, "%a, %d-%b-%y %H:%M:%S GMT")

        serializer = self.get_serializer(instance)
        response = Response(serializer.data, status=status.HTTP_200_OK)

        # 쿠키 읽기 & 생성
        if request.COOKIES.get('hits') is not None:  # 쿠키가 있을 경우
            cookies = request.COOKIES.get('hits')
            cookies_list = cookies.split('|')
            if str(pk) not in cookies_list: # 쿠키에 현재 게시글물이 없을 경우(게시물을 처음 조회 했을 경우)
                with transaction.atomic():
                    response.set_cookie('hits', cookies + f'|{pk}', expires=expires)
                    instance.hits += 1
                    instance.save()
                    return response

        else:  # 쿠키가 없을 경우
            response.set_cookie('hits', pk, expires=expires) # hits란 이름의 쿠키와 pk를 value로 저장
            instance.hits += 1
            instance.save()
            return response

        serializer = self.get_serializer(instance)
        response = Response(serializer.data, status=status.HTTP_200_OK)

        return response

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()

    @action(detail=True, methods=['put'])
    def likes(self, request, pk=None):
        """각 게시글에 좋아요하는 endpoint"""

        user = request.user

        data = {
            'post_id': pk,
            'user_id': user.id
        }

        serializer = PostingLikeSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        like_object = Like.objects.filter(user_id=user, post_id=pk)

        if not like_object.exists():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            like_object.delete()
            return Response('좋아요가 취소되었습니다', status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['put'])
    def restores(self, request, pk=None):
        """게시글의 작성자만 삭제된 게시글을 복구할 수 있는 endpoint"""

        user = request.user
        posting_instance = get_object_or_404(Posting, pk=pk)

        data = {
            'id': pk,
            'user_id': user.id
        }

        serializer = PostingRestoreSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        if posting_instance.user_id != user:
            return Response('ERROR : 게시글에 대한 접근 권한이 없습니다.', status=status.HTTP_400_BAD_REQUEST)
        else:
            if posting_instance.is_delete == 1:
                posting_instance.is_delete = 0
                posting_instance.save()
                return Response('RESTORE : 게시글을 성공적으로 복구하였습니다.', status=status.HTTP_200_OK)
            else:
                return Response('ERROR : 이미 처리된 게시글입니다.', status=status.HTTP_400_BAD_REQUEST)
