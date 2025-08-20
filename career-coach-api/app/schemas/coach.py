from pydantic import BaseModel, Field
from typing import List

class CareerCoachRequest(BaseModel):
    careerSummary: str = Field(..., description="경력 요약 (예: 3년차 백엔드 개발자)")
    jobDuties: str = Field(..., description="수행 직무 및 프로젝트 (예: Spring Boot 기반 커머스 서비스 개발 및 운영)")
    technicalSkills: List[str] = Field(..., description="보유 기술 스킬 (예: ['Java', 'Spring Boot', 'Python', 'MSA', 'AWS'])")

class CareerCoachResponse(BaseModel):
    interviewQuestions: List[str] = Field(..., description="맞춤형 면접 질문 5개")
    learningPath: str = Field(..., description="개인화된 학습 경로 및 액션 플랜 (마크다운 형식)")
