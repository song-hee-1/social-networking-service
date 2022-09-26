from rest_framework import serializers

from apps.postings.models import Posting, Hashtag


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
    like_num = serializers.ReadOnlyField(source='like.like_num')
    hashtag = HashtagSerializer(many=True)

    class Meta:
        model = Posting
        fields = ['title', 'user_id', 'hashtag', 'create_time', 'like_num', 'hits']


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
    class Meta:
        model = Posting
        fields = '__all__'
