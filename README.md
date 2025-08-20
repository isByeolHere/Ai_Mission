## Ai_Mission – Career Coach API

생성형 AI(Google Gemini)를 활용해 이력서 정보를 입력하면 맞춤형 기술 면접 질문과 개인화 학습 경로를 제안하는 FastAPI 기반 백엔드 서비스입니다.

### 주요 기능

- **맞춤형 면접 질문 생성**: 이력서 기반 심층 면접 질문 5개 자동 생성
- **개인화 학습 경로**: 강점/보완점 분석 후 실행 가능한 액션 플랜을 마크다운으로 제공

### 디렉터리 구조

```
Ai_Mission/
  └─ career-coach-api/
      ├─ app/
      │  ├─ api/v1/endpoints/coach.py        # 코칭 API 엔드포인트
      │  ├─ schemas/coach.py                 # 요청/응답 스키마
      │  ├─ services/career_coach.py         # Gemini 연동 서비스 로직
      │  └─ main.py                          # FastAPI 앱 엔트리포인트
      ├─ requirements.txt
      └─ static/index.html                   # 랜딩 페이지
```

### 빠른 시작

1. 의존성 설치 (Python 3.11+ 권장)

```bash
cd career-coach-api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. 환경 변수 설정 (`.env` 생성)

```bash
echo "GOOGLE_API_KEY=YOUR_GEMINI_API_KEY" > .env
```

3. 로컬 서버 실행

```bash
uvicorn app.main:app --reload
```

실행 후:

- 웹 랜딩: `http://127.0.0.1:8000/`
- API 베이스: `http://127.0.0.1:8000/api/v1/coach/`

### API 사용법

- **엔드포인트**: `POST /api/v1/coach/`
- **요청 바디**

```json
{
  "careerSummary": "3년차 백엔드 개발자",
  "jobDuties": "Spring Boot 기반 커머스 서비스 개발 및 운영",
  "technicalSkills": ["Java", "Spring Boot", "Python", "MSA", "AWS"]
}
```

- **응답 예시(요약)**

```json
{
  "interviewQuestions": ["...5개 질문..."],
  "learningPath": "# 분석 및 추천\n...마크다운 형식의 액션 플랜..."
}
```

- **cURL 예시**

```bash
curl -X POST \
  http://127.0.0.1:8000/api/v1/coach/ \
  -H "Content-Type: application/json" \
  -d '{
    "careerSummary": "3년차 백엔드 개발자",
    "jobDuties": "Spring Boot 기반 커머스 서비스 개발 및 운영",
    "technicalSkills": ["Java", "Spring Boot", "Python", "MSA", "AWS"]
  }'
```

### 환경 변수

- **GOOGLE_API_KEY**: Google Gemini API 키 (필수)
- 사용 모델: `gemini-1.5-flash`

### 참고

- 루트(`/`)와 `/docs`는 프로젝트의 정적 랜딩 페이지(`static/index.html`)를 보여줍니다.
- 실제 API 호출은 `POST /api/v1/coach/`를 사용하세요.
