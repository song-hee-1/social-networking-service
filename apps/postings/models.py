from django.db import models
from django.contrib.auth import get_user_model


class Posting(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name="postings", null=True,
                                db_column="user_id")
    title = models.CharField(max_length=72, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    hits = models.PositiveIntegerField(verbose_name="조회수", default=0)
    hashtag = models.ManyToManyField("HashTag", db_column="hashtag_id")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="게시글 생성 날짜")
    update_time = models.DateTimeField(auto_now=True, verbose_name="게시글 수정 날짜")
    is_delete = models.BooleanField(verbose_name="삭제 여부", default=0)
    likes = models.ManyToManyField(
        get_user_model(),
        through="Like",
        related_name="posting_likes",
        blank=True,
        verbose_name="좋아요 내역"
    )

    class Meta:
        verbose_name = "게시글"
        verbose_name_plural = "게시글 목록"
        db_table = 'posting'

    def __str__(self):
        return self.title


class Like(models.Model):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, db_column="user_id", null=True)
    post_id = models.ForeignKey("Posting", on_delete=models.CASCADE, db_column="post_id")
    # like_num = models.PositiveIntegerField(verbose_name="좋아요 수")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="좋아요 한 날짜")

    class Meta:
        unique_together = ('user_id', 'post_id')
        verbose_name = "좋아요"
        verbose_name_plural = "좋아요 목록"
        db_table = 'like'

    def __str__(self):
        return self.post_id


class Hashtag(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = "해시태그"
        verbose_name_plural = "해시태그 목록"
        db_table = "hashtag"

    def __str__(self):
        return self.name
