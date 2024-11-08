# Test Ground for Advanced Python Library

## ORM
### SQL Model
FastAPI 제작자가 만든 ORM 으로 SQLAlchemy 와 Pydantic 을 결합해 구성한 라이브러리이다
SQLAlchemy 보다 더 추상적으로 사용할 수 있어 같은 기능을 구현하더라도 더 짧은 코드와 불필요한 LocalSession 재구성이 필요 없다
FastAPI 에서 사용을 염두해두었기 때문에 API 에서 입력 값을 검증하는 Pydantic 모델을 ORM 의 테이블 Model 로 대체할 수 있어 Table 클래스 작성 시 재사용이 가능하다

### asyncmy
ORM 의 비동기 처리를 위한 MySQL/MariaDB 용 비동기 커넥터로 PyMySQL, aiomysql 의 코드를 재사용하여 안정성이 보장되었고 Cython 으로 개발되어 성능상 이점이 있다
최신 버전이 23년 릴리즈에 MySQL 7.x 버전까지 공식으로 지원한다고 되어 있어 향후 호환성 문제가 생길 수 있다
타 RDBMS 사용 시 커넥터를 변경하면되므로 이 부분은 협소한 문제이다

## Logging
### picologging
Microsoft 에서 개발하는 로깅 라이브러리로 기본 내장 logging 모듈보다 최소 4배 이상 빠르다고 한다
아직 beta 임을 명시하고 있어 프로덕션에선 활용이 힘들다
기본적인 기능 사용법이 loguru 대비 복잡한 편이며, 커스텀 로그 포멧도 제한된다
향후 stable 버전 릴리즈 및 기능이 추가되면 점진적으로 적용해 볼만 하다

## Settings
### pydantic-settings
여러 시크릿 파일을 불러오기에는 적합해보이나 1~2개 파일로 시크릿 정보를 관리한다면 불필요하다
스크릿 정보를 pydantic 으로 타입 안전하게 불러올 수 있으나 Model 클래스 작성에 따른 중복 작성 문제, 간단한 기능 대비 과도한 설정 필요와 같은 문제가 있다