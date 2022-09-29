from django.core.exceptions import ValidationError


def validate_hashtag_name(value):
    if not value.startswith("#"):
        message = "해시태그는 #로 시작해야 합니다."
        raise ValidationError(message=message)
    else:
        return value
