from rest_framework.test import APITestCase

from django.urls import reverse

from apps.accounts.models import User


class UserLoginTest(APITestCase):
    """ 이메일로 로그인 할 수 있는지 확인하기 위한 테스트 """

    def setUp(self):
        User.objects.create_user(
            username="핑핑", password="0000", email="test@test.com"
        )

    def test_fail_login_username(self):
        response = self.client.login(username="핑핑", password="0000")
        self.assertEquals(response, False)

    def test_success_login_email(self):
        response = self.client.login(email="test@test.com", password="0000")
        self.assertEquals(response, True)


class GetJWTTokenTest(APITestCase):
    """ 로그인시 JWT Token 발급이 정상적오르 작동하는지 확인하기 위한 테스트 """

    def setUp(self):
        User.objects.create_user(
            username="핑핑", password="0000", email="test@test.com"
        )

    def test_login_get_token(self):
        data = {
            'email': 'test@test.com',
            'password': '0000'
        }
        response = self.client.post(reverse('rest_login'), data)
        access_token = response.data["access_token"]
        self.assertFalse(access_token is None)
