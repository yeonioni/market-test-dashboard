# Market Data Report v1.0

Google Analytics와 Meta API를 연동하여 마케팅 캠페인 데이터를 분석하는 웹 애플리케이션입니다.

## 🚀 주요 기능

- Google Analytics 데이터 수집
- Meta 광고 캠페인 데이터 수집
- 캠페인별 성과 지표 분석
- 웹 기반 리포트 생성

## 📋 필수 요구사항

- Python 3.7+
- Google Analytics 4 프로퍼티
- Meta Business 계정 및 액세스 토큰

## 🔧 설치 및 설정

### 1. 저장소 클론
```bash
git clone <repository-url>
cd marketdata_report.v.1.0
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

### 3. 의존성 설치
```bash
pip install flask google-analytics-data requests python-dotenv
```

### 4. 환경 변수 설정

`env.example` 파일을 참고하여 `.env` 파일을 생성하고 필요한 값들을 설정하세요:

```bash
cp env.example .env
```

`.env` 파일에 다음 정보를 입력하세요:

```env
# Google Analytics 설정
GA_PROPERTY_ID=your_ga_property_id_here

# Meta API 설정
META_ACCESS_TOKEN=your_meta_access_token_here
META_AD_ACCOUNT_ID=your_meta_ad_account_id_here
META_API_VERSION=v19.0
```

### 5. Google Analytics 서비스 계정 키 설정

1. Google Cloud Console에서 서비스 계정 생성
2. Google Analytics API 활성화
3. 서비스 계정 키 다운로드
4. `ga_key.json` 파일명으로 프로젝트 루트에 저장

⚠️ **보안 주의사항**: `ga_key.json` 파일은 `.gitignore`에 포함되어 Git에 업로드되지 않습니다.

## 🚀 실행 방법

```bash
python app.py
```

애플리케이션이 `http://localhost:8888`에서 실행됩니다.

## 📊 사용 방법

1. 웹 브라우저에서 `http://localhost:8888` 접속
2. 키워드 입력하여 캠페인 검색
3. 분석할 캠페인 선택
4. 페이지 경로 및 클릭 데이터 입력
5. 리포트 생성 및 확인

## 🔒 보안 고려사항

- API 키와 인증 정보는 환경 변수로 관리
- 서비스 계정 키 파일은 Git에 업로드하지 않음
- 프로덕션 환경에서는 HTTPS 사용 권장

## 📁 프로젝트 구조

```
marketdata_report.v.1.0/
├── app.py              # Flask 메인 애플리케이션
├── ga_api.py           # Google Analytics API 연동
├── meta_api.py         # Meta API 연동
├── templates/          # HTML 템플릿
├── .gitignore          # Git 제외 파일 목록
├── env.example         # 환경 변수 예시
└── README.md           # 프로젝트 문서
```

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 