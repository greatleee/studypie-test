## 환경
* python 3.8.2

## 실행 방법

1. 사용 패키지 설치
```bash
pip install -r requirements.txt
```

2. 포인트, 알람 (Q2, Q3) 패키지 설치
```bash
cd studypie-alarms
python setup.py sdist
pip install dist/studypie-alarms-0.1.tar.gz
cd ..
cd studypie-points
python setup.py sdist
pip install dist/studypie-points-0.1.tar.gz
```

3. 실행
```bash
python manage.py runserver
```

## 테스트 코드 실행방법
* studypie-points만 테스트코드가 존재합니다.
```bash
cd studypie-points
pytest
```
