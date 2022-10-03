# Social Networking Service

사용자는 **게시물**을 **업로드** 하거나, 다른 사람의 게시물을 확인하고 **좋아요**를 누를 수 있는 **SNS 서비스**
</br>

## 목차

  * [개발 기간](#개발-기간)
  * [프로젝트 개요](#프로젝트-개요)
      - [프로젝트 주체](#프로젝트-주체)
      - [💭 프로젝트 설명](#-프로젝트-설명)
      - [🛠 개발 조건](#-개발-조건)
      - [🧹 사용 기술](#-사용-기술)
      - [📰 모델링](#-모델링)
      - [🛠 API Test](#-api-test)
  * [프로젝트 분석](#프로젝트-분석)
  * [API ENDPOINT](#api-endpoint)
  * [Troubleshooting](#troubleshooting)
  * [TIL](#til)



</br>

## 개발 기간
**2022.09.26 ~ 2022.10.01** 

</br>
</br>
  
## 프로젝트 개요


#### 프로젝트 주체 

![image](https://user-images.githubusercontent.com/83492367/193399733-f831e18f-5764-41c4-94c9-fa86e301e81c.png)



[원티드 - 프리온보딩](https://www.wanted.jobs/events/pre_ob_be_4)

</br>

#### 💭 프로젝트 설명

서비스 개요 및 요구사항을 만족하는 **SNS(Social Networking Service) 백엔드 서비스** 구현

</br>

#### 🛠 개발 조건



> * **유저관리**
> 	* 유저 회원가입 : 이메일을 ID로 사용
> 	* 유저 로그인 및 인증 : JTW 토큰을 발급하여 사용자 인증으로 사용


> * **게시글**
> 	- 게시글 생성
> 		* 제목, 내용, 해시태그 등을 입력하여 생성
> 		* 제목, 내용, 해시태그는 필수 입력사항이며, 작성자 정보는 request body에 존재하지 않고, 해당 API 를 요청한 인증정보에서 추출하여 등록
> 		* 해시태그는 #로 시작되고 , 로 구분되는 텍스트가 입력됩니다.
> 	- 게시글 수정
> 		- 작성자만 수정 가능
> 	- 게시글 삭제
> 		- 작성자만 삭제 가능
> 		- 작성자는 삭제된 게시글을 다시 복구 가능
> 	- 게시글 상세보기
> 		- 모든 사용자는 모든 게시물에 보기권한
> 		- 작성자를 포함한 사용자는 본 게시글에 좋아요 누를 수 있음
> 		- 좋아요된 게시물에 다시 좋아요를 누르면 취소
> 		- 작성자를 포함한 사용자가 게시글을 상세보기하면 조회수가 1 증가
> 	- 게시글 목록
> 		- 모든 사용자는 모든 게시물에 보기 권한
> 		- 게시글 목록에는 제목, 작성자, 해시태그, 작성일, 좋아요 수, 조회수가 포함
> 		- 아래의 4가지 동작은 쿼리 파라미터로 구현하며 동시에 적용가능
> 			1. Ordering (= Sorting, 정렬)
				- default : 작성일
				- 사용자가 작성일, 좋아요 수, 조회수 중 1개만 선택하여 값 정렬가능
				- 오름차, 내림차 순을 선택 가능

>			2. Searching (= 검색)
> 				- 해당 키워드가 제목에 포함된 게시글 목록
> 
> 			3. Filtering (= 필터링)
> 				- 해당 키워드의 해시태그를 포함한 게시물 필터링
> 
> 			4. Pagination (= 페이지 기능)
> 				- default : 10건
> 				- 사용자는 1 페이지 당 게시글 수 조정 가능



</br>

#### 🧹 사용 기술 

- **Back-End** : Python, Django, Django REST
Framework, Dj Rest Auth, Django Allauth, Djangorestframework Simplejwt
- **Database** : SQLite
- **ETC** : Git, Github

</br>



#### 📰 모델링

![Untitled (1)](https://user-images.githubusercontent.com/83492367/193401293-634f741a-eee3-4a41-b3de-360bf5d08c35.png)


- 서비스 흐름을 고려하여 `User(사용자)`, `Posting(게시글)`, `HashTag(해시태그)`의 테이블로 모델링
- `User(사용자)` 와 `Posting(게시글)`은 **M:N**의 관계로  `Like(좋아요) `라는 **중간 테이블**을 가짐
	- 좋아요를 누른 시간을 기록하기 위하여  `through `를 통하여  **중간 테이블 직접 지정**
- `Posting(게시글)`과 `Hashtag(해시태그)`는 **M:N**의 관계로 `Posting_Hashtag ` 중간 테이블 자동 생성
- `hits(조회수)`의 경우 음수가 될 수 없으므로 `PositiveIntegerField`를 이용하여 모델링


</br>

#### 🛠 API Test

- 유저관리 : 이메일을 ID로 사용하는지,  JWT Token이 제대로 발급되는지 확인하는 테스트 코드 작성

- 게시글 : 게시글의 CRUD(ViewSet Action)이 정상 작동하는지 확인하는 테스트 코드 작성

![image](https://user-images.githubusercontent.com/83492367/193399920-09d831e2-8937-408b-88e1-4d96749f39a6.png)




</br>

## 프로젝트 분석
- 개발 조건과 확장성을 고려하여 `accounts`, `postings` 의 2개의 앱으로 분리
- JWT 토큰 발급은 `djangorestframework-simplejwt` 이용 
	- `djangorestframework-jwt`는 최신 업데이트가 진행되지 않으므로 이용 X
	- `Access Token`은 2시간, `Refresh Token`은 일주일의 유효기간
- `dj-rest-auth`와 `django-allauth`를 회원가입, 로그인, 비밀번호 찾기 등의 기능 이용

- 게시글 생성
	- 게시글 생성 시 `get_or_create`를 통해 기존 해시태그를 가져오거나,새로운 해시태그이면 해시태그 객체를 생성하여 저장
	- 게시글 생성 시 `access token`을 바탕으로 사용자 정보를 식별하여 **작성자 정보가 자동 저장**됨
- 게시글 목록 및 상세보기
	- 게시글의 좋아요는 잦은 변동이 예상되므로 `Serializer Method Field`로 계산
	- 게시글 상세보기시 조회수가 **단순히 +1**되도록 구현
	-  그 결과 새로고침시 마다 조회수가 무분별하게 증가되는 문제 발생
	- 게시글 상세보기시 무분별한 조회수 증가 방지를 위하여 `Cookie`를 이용하여 **일1회만 조회수 증가**
	- `정렬`,`검색`, `필터링`, `페이지 기능` 은 `Django Q 모델`을 이용하여 구현
		- `q.add`를 통해 여러 조건을 연산하므로 각 조건은 독립적으로도,  조합하여서도 사용 가능 
		- `정렬`은 `?ordering={필드명}으로 `오름차순`이며, `-`를 이용하여 `내림차순` 이용 가능
		- `검색`은 `?search=후기`로 제목에 포함된 키워드로 검색 가능
		- `필터링`은 `?hashtags=서울` 혹은 `?hashtags=서울&hashtags=맛집`으로 1개, 2개 이상 검색 가능
		- `페이지 기능`은 기본 10개로, `?page_size={원하는 개수}`를 이용하여 조정 가능
- 게시글 삭제 후 복구를 위하여 `is_delete`를 이용한 **soft delete** 구현
	- 삭제된 게시글 복구는 @action decorator를 이용하여 복구 가능


	

	
</br>

## API ENDPOINT

### accounts - User

URL|Method|Action|Description|
|------|---|---|---|
|api/accounts/users|GET|List|사용자 전체 목록 조회|
|api/accounts/users/int:pk|GET|Retrieve|사용자 세부내역 조회|
|api/accounts/users/int:pk|PUT|Update|사용자 세부내역 업데이트|
|api/accounts/users/int:pk|PATCH|Partial_Update|사용자 세부내역 부분 업데이트|

### accounts - Dj Rest Auth

URL|Method|Description|
|------|---|---|
|api/accounts/password/reset|POST|이메일을 통한 사용자 비밀번호 재설정|
|api/accounts/password/reset/confirm|POST|사용자 비밀번호 재설정 및 새로운 토큰 발급|
|api/accounts/password/change|POST|기존 비밀번호를 통해 비밀번호 재설정|
|api/accounts/login|POST|사용자 로그인(토큰 반환)|
|api/accounts/logout|POST|사용자 로그아웃|
|api/accounts/token/verify|POST|토큰 유효성 확인|
|api/accounts/token/refresh|POST|refresh 토큰을 통한 access 토큰 재발급|
|api/accounts/registration|POST|사용자 회원가입|



### postings


URL|Method|Action|Description|
|------|---|---|---|
|api/accounts/posintgs|GET|List|게시글 전체 목록 조회|
|api/accounts/posintgs/int:pk|GET|Retrieve|게시글 세부내역 조회
|api/accounts/posintgs/int:pk|PUT|Update|게시글 세부내역 업데이트|
|api/accounts/posintgs/int:pk|PATCH|Partial_Update|게시글 세부내역 부분 업데이트|
|api/accounts/posintgs/int:pk/likes|PUT|@action|각 게시글에 좋아요|
|api/accounts/posintgs/int:pk/likes/restores/|PUT|@action|삭제된 게시글 복구|

* 각 게시글에 좋아요, 삭제된 게시글 복구는 @action decorator 이용


</br>

## Troubleshooting

<details>
<summary>데이터 필터링: ORM query parameter</summary>

<!-- summary 아래 한칸 공백 두어야함 -->


- 해시태그를 1개 검색하는데에는 큰 어려움이 없었으나 2개 이상 검색하는 기능을 구현하기 위해서 거의 3-4일을 소비함
- Q 객체를 이용하여 filter하는 방식을 이용하였는데, 같은 필드를 AND 조건으로 검색할 시 filtering이 제대로 이루어지지 않음
- shell에서 데이터에 직접적으로 접근하여 filter를 해보아도 OR 조건만 정상 작동하고 AND 조건이 제대로 작동하지 않음
![image](https://user-images.githubusercontent.com/83492367/193531099-24632a67-54f8-4ee3-9603-c75e9cf5c18e.png)
- Q 객체를 이용하지 않고 조건을 연속으로 filtering하였을 때는 정상적으로 작동함
- 원인을 알고 싶어 여러방법으로 구현해보고 탐구를 해보았으나 **기한안에 ** 직접적인 원인을 찾지 못함
- 결과적으로는 parameter를 `getlist`를 통해 list 형식으로 받고, 각 값을 for loop로 돌면서 연속으로 filering하는 방법으로 구현
- 무슨 이유로 작동하지 않았는지 궁금하며, ORM의 데이터 구조와 관련이 있을 것 같은 예측이 들어 그 부분에 대해 **추후 학습 예정**


</details>



</br>


## TIL

- [[TIL] ModuleNotFoundError: No module named ‘django’ 에러 해결하기 2탄](https://medium.com/@heeee/til-modulenotfounderror-no-module-named-django-%EC%97%90%EB%9F%AC-%ED%95%B4%EA%B2%B0%ED%95%98%EA%B8%B0-2%ED%83%84-27246e545d8b)]
- [[TIL] DRF 동적 pagination 만들기 (한페이지 당 데이터 개수 조정)](https://medium.com/@heeee/til-drf-%EB%8F%99%EC%A0%81-pagination-%EB%A7%8C%EB%93%A4%EA%B8%B0-%ED%95%9C%ED%8E%98%EC%9D%B4%EC%A7%80-%EB%8B%B9-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EA%B0%9C%EC%88%98-%EC%A1%B0%EC%A0%95-6f1e2f2e973c)
- [[TIL] DRF APITestCase Post시 400 에러 해결하기 ( + JWT Token)](https://medium.com/@heeee/til-drf-apitestcase-post%EC%8B%9C-400-%EC%97%90%EB%9F%AC-%ED%95%B4%EA%B2%B0%ED%95%98%EA%B8%B0-jwt-token-c8368f89b0ad)
- [[Django] Django(DRF)에서 Dj-Rest-Auth와 SimpleJWT 잘 사용하기( Dj-Rest-Auth와 SimpleJWT의 의존성)](https://medium.com/@heeee/django-django-drf-%EC%97%90%EC%84%9C-dj-rest-auth%EC%99%80-simplejwt-%EC%9E%98-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0-dj-rest-auth%EC%99%80-simplejwt%EC%9D%98-%EC%9D%98%EC%A1%B4%EC%84%B1-88c80bf4fb0f)






