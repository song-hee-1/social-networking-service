from rest_framework import serializers

from apps.postings.models import Posting, Hashtag, Like


# 해시태그
class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['name']
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'validators': []},  # 중복된 hashtag도 허용하기 위해서 validator 제거
        }


# 게시글 목록
class PostingListSerializer(serializers.ModelSerializer):
    like_num = serializers.SerializerMethodField()
    hashtag = HashtagSerializer(many=True)

    class Meta:
        model = Posting
        fields = ['title', 'user_id', 'hashtag', 'create_time', 'like_num', 'hits']

    def get_like_num(self, instance):
        return instance.likes.count()


# 게시글 생성
class PostingCreateSerializer(serializers.ModelSerializer):
    hashtag = HashtagSerializer(many=True)

    class Meta:
        model = Posting
        fields = ['title', 'content', 'hashtag']
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        hashtags = validated_data.pop('hashtag', None)

        if not hashtags:
            raise serializers.ValidationError('ERROR: 해시태그는 필수 입력값입니다')

        posting = Posting.objects.create(**validated_data)

        for hashtag in hashtags:
            hashtag, is_created = Hashtag.objects.get_or_create(name=hashtag['name'])
            posting.hashtag.add(hashtag)
        return posting


# 게시글 상세보기
class PostingDetailSerializer(serializers.ModelSerializer):
    like_num = serializers.SerializerMethodField()

    class Meta:
        model = Posting
        fields = '__all__'

    def get_like_num(self, instance):
        return instance.likes.count()


# 좋아요
class PostingLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ['create_time']


# 삭제된 게시글 복구
class PostingRestoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posting
        fields = ['id', 'user_id']
