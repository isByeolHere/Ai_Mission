# Career Coach API

AI 기반 개인 맞춤형 커리어 코칭을 제공하는 FastAPI 기반 REST API입니다.

## 주요 기능

- **맞춤형 면접 질문 생성**: 사용자의 경력과 기술 스택을 바탕으로 한 심층 면접 질문 5개 생성
- **개인화된 학습 경로**: 현재 역량을 분석하여 구체적인 성장 액션 플랜 제시
- **OpenAI GPT-4o 통합**: 최신 AI 모델을 활용한 고품질 코칭 제공

## 기술 스택

- **Backend Framework**: FastAPI
- **AI Model**: OpenAI GPT-4o
- **Async Processing**: asyncio를 활용한 동시 API 호출
- **Data Validation**: Pydantic 모델
- **Environment Management**: python-dotenv

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 OpenAI API 키를 설정하세요:

```bash
# .env 파일 생성
echo 'OPENAI_API_KEY="your_actual_api_key_here"' > .env
```

### 3. 서버 실행

```bash
uvicorn app.main:app --reload
```

서버는 `http://localhost:8000`에서 실행됩니다.

## API 사용법

### POST /api/v1/coach/

커리어 코칭을 요청하는 엔드포인트입니다.

**Request Body:**

```json
{
  "careerSummary": "3년차 백엔드 개발자",
  "jobDuties": "Spring Boot 기반 커머스 서비스 개발 및 운영, AWS EC2 환경에서 서비스 배포",
  "technicalSkills": ["Java", "Spring Boot", "Python", "MSA", "AWS", "JPA"]
}
```

**Response:**

```json
{
  "interviewQuestions": ["질문1", "질문2", "질문3", "질문4", "질문5"],
  "learningPath": "마크다운 형식의 개인화된 학습 경로..."
}
```

## API 문서

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 프로젝트 구조

```
career-coach-api/
├── app/
│   ├── api/v1/endpoints/    # API 엔드포인트
│   ├── schemas/             # Pydantic 데이터 모델
│   ├── services/            # 비즈니스 로직
│   └── main.py             # FastAPI 애플리케이션
├── requirements.txt         # Python 의존성
└── .env                    # 환경 변수 (사용자 생성 필요)
```

## 개발 가이드

### 새로운 기능 추가

1. `app/schemas/`에 새로운 데이터 모델 정의
2. `app/services/`에 비즈니스 로직 구현
3. `app/api/v1/endpoints/`에 새로운 엔드포인트 추가

### 테스트

```bash
# 테스트 실행 (pytest 설치 필요)
pytest

# 코드 품질 검사
flake8 app/
black app/
```

## 라이선스

MIT License

## 기여 방법

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
