from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from apps.accounts.models import User


class PostingViewSetTest(APITestCase):
    """ Posting ViewSet이 정상작동하는지 확인하는 테스트 """

    def setUp(self):
        User.objects.create_user(
            username="핑핑", password="0000", email="test@test.com"
        )
        login_data = {'email': 'test@test.com', 'password': '0000'}
        response = self.client.post(reverse('rest_login'), login_data)
        access_token = response.data["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        data = {
            "title": "게시글 생성 테스트 첫번째 제목",
            "content": "게시글 생성 테스트 첫번째 본문",
            "hashtag": [
                {"name": "#해시태그테스트1"}
            ]
        }

        response = self.client.post(reverse('postings-list'), data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_posting_create(self):
        data = {
            "title": "게시글 생성 테스트 두번째 제목",
            "content": "게시글 생성 테스트 두번째 본문",
            "hashtag": [
                {"name": "#해시태그테스트2"}
            ]
        }

        response = self.client.post(reverse('postings-list'), data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_posting_get_list(self):
        response = self.client.get(reverse('postings-list'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_posting_get_retrieve(self):
        response = self.client.get(reverse('postings-detail', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_posting_update(self):
        update_data = {
            "title": "게시글 수정 테스트",
        }
        response = self.client.patch(reverse('postings-detail', kwargs={'pk': 1}), update_data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_posting_destory(self):
        response = self.client.delete(reverse('postings-detail', kwargs={'pk': 1}))
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
