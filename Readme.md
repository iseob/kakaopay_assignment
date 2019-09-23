## KakaoPay Assginment

### 개발 프레임워크
+ 언어는 python 3.7.4을 사용하였고, 프레임워크는 django를 사용하였습니다.  
+ 더 들어가서는 rest api를 만들수 있게 도와주는 django-rest-framework이라는 라이브러리를 사용하였습니다.  
+ 테스트는 pytest라는 모듈을 사용하였습니다.  
+ Postgresql, Redis는 docker를 활용해서 띄우고 프레임워크에서 연결해서 사용하였습니다.  

### 문제해결 전략
샘플 데이터 db에 저장
> + csv라는 모듈을 활용해서 해당 데이터 파일을 열고, 파싱해서 각 row를 create하는 클래스 메소드를 만들어서 실행하게 하였습니다.

TPS handle
> + Redis를 사용해서 같은 db 쿼리에 대해서 캐싱을 하게 하였습니다.
> + WHERE 문에 들어가거나 ORDER_BY 에 들어가는 column 들은 모두 index를 추가해놨습니다. 
> + 추가로, API 기능 명세에서 upsert 혹은 delete 하는 API가 없어서 따로 lock 방지를 위해 replication은 하지 않았습니다.



### 못한 부분
미처 다 끝내지 못한 부분이 총 두군데 입니다. 그리고 그에 따라 어떻게 할 것이었는지에 대한 설명입니다.  

유저 생성 및 jwt 활용
> + 유저는 장고에서 제공해주는 abstractUser 모델을 상속 및 커스터마이즈해서 생성합니다.
> + jwt는 djangorestframework-jwt 라는 라이브러리를 사용합니다.
> + signup이나 signin을 제외하고는 permission을 겁니다.

2019년도 이용률 예측
> + 해당 디바이스의 각 연도별 이용률에 대한 기울기를 구합니다.
> + 그리고 해당 기울기들을 가지고 linear한 함수에 대입하여 다음 기울기를 예측합니다.
> + 예측된 기울기와 마지막 연도의 이용률을 가지고, 2019년의 이용률을 예측합니다. 

성능을 고려해서 10000 TPS handle
> + aws 같은 곳에 올렸을때, ec2 인스턴스를 여러개 두고 앞단에 로드 밸런서를 달아서 부하를 방지합니다.(멀티 프로세싱)  
> + db 쿼리에 redis를 걸어놓는 것보다 로컬의 버퍼사이즈만큼 key value store를 이용해서  
> upsert 혹은 delete 될때마다 해당 store를 업데이트 하면서 db와 싱크를 맞추는 방향으로 해볼 것입니다.  
> + 그외에 필요하다면 replication을 추가해놓을 것 입니다.

### 빌드 및 실행 방법
#### commands
`brew install pipenv`  
`pipenv --python 3.7.4`  
`pipenv shell`  
`pipenv install`  
`docker-compose -f docker-compose.yml up`  
`python kakaopay_assignment/manage.py makemigrations`  
`python kakaopay_assignment/manage.py migrate`  
`python kakaopay_assignment/manage.py create_basic_data`  
`python kakaopay_assignment/manage.py runserver`  

#### 추가설명
테스트 실행 : `pytest`  
제공된 통계 데이터는 root에 stat_data.csv로 존재하고, device 테이블 데이터는 device_data.csv입니다.  
빌드 및 실행 그리고 테스트 실행은 root에서 kakaopay_assignment라는 디렉토리로 들어가서 하시면 됩니다.  
감사합니다.
