from app.schemas.coach import CareerCoachRequest, CareerCoachResponse
import asyncio
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Google Gemini client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

class CareerCoachService:
    async def get_coaching_advice(self, request: CareerCoachRequest) -> CareerCoachResponse:
        questions_task = self._generate_interview_questions(request)
        learning_path_task = self._generate_learning_path(request)

        generated_questions, generated_path = await asyncio.gather(
            questions_task,
            learning_path_task
        )

        return CareerCoachResponse(
            interviewQuestions=generated_questions,
            learningPath=generated_path
        )

    async def _generate_interview_questions(self, request: CareerCoachRequest) -> list[str]:
        prompt = f"""
        당신은 현대 클라우드 네이티브 아키텍처에 정통한 15년차 시니어 백엔드 개발자이자, 기술 면접관입니다. 당신의 임무는 지원자가 제출한 이력서 정보를 바탕으로, 깊이 있고 통찰력 있는 심층 면접 질문 5개를 생성하는 것입니다.
        이 질문들은 절대로 일반적인 기술 상식을 묻는 질문이어서는 안 됩니다. 대신, 지원자의 실제 실무 경험, 문제 해결 능력, 기술적 의사결정 과정을 파고드는 날카로운 상황 기반 질문이어야 합니다. 질문은 지원자가 STAR 기법(Situation, Task, Action, Result)에 기반하여 답변하도록 유도해야 합니다.

        [지원자 정보]
        - 경력 요약: {request.careerSummary}
        - 수행 직무 및 프로젝트: {request.jobDuties}
        - 보유 기술 스킬: {", ".join(request.technicalSkills)}

        [지시사항]
        1. 경험과 직접적으로 연결: 모든 질문은 지원자의 '수행 직무 및 프로젝트'와 '보유 기술 스킬'을 명시적으로 결합하여 만들어야 합니다.
        2. '왜'와 '어떻게'에 집중: 지원자가 '무엇을' 했는지보다, '왜' 그런 기술적 결정을 내렸는지, 그리고 특정 문제를 '어떻게' 해결했는지에 초점을 맞추세요.
        3. 현실적인 시나리오 구성: 질문은 지원자가 실제로 겪었을 법한 현실적인 시나리오 형식으로 제시되어야 합니다.
        4. 단순한 정의 질문 금지: 기술의 정의를 묻지 마세요. (예: "MSA란 무엇인가요?") 대신, 기술의 적용 사례를 질문하세요. (예: "MSA 기반 커머스 서비스 개발 경험에서, 여러 마이크로서비스 간의 데이터 일관성은 어떻게 해결하셨나요?")
        5. 출력 형식: 결과물은 5개의 문자열을 담은 JSON 배열 형식으로만 출력해야 합니다. ["질문1", "질문2", "질문3", "질문4", "질문5"]

        이제 위 지시사항에 따라, 주어진 지원자 정보를 바탕으로 면접 질문 5개를 생성해 주세요.
        """

        try:
            # Google Gemini API 호출
            response = await asyncio.to_thread(
                model.generate_content,
                prompt
            )
            content = response.text
            
            # JSON 응답 파싱
            try:
                question_list = json.loads(content)
                if isinstance(question_list, list) and len(question_list) > 0:
                    return question_list
                else:
                    return ["AI 모델로부터 유효한 질문 목록을 생성하지 못했습니다."]
            except json.JSONDecodeError:
                # JSON 파싱 실패 시 텍스트에서 질문 추출 시도
                lines = content.strip().split('\n')
                questions = []
                for line in lines:
                    line = line.strip()
                    if line and (line.startswith('"') or line.startswith('-') or line.startswith('•')):
                        # 따옴표나 불릿 포인트 제거
                        question = line.strip('"').strip('-').strip('•').strip()
                        if question and len(question) > 10:
                            questions.append(question)
                        if len(questions) >= 5:
                            break
                
                if questions:
                    return questions[:5]
                else:
                    return ["AI 모델로부터 유효한 질문 목록을 생성하지 못했습니다."]
                    
        except Exception as e:
            print(f"Error generating interview questions: {e}")
            return ["AI 모델 호출 중 오류가 발생했습니다. API 키와 서버 상태를 확인해주세요."]

    async def _generate_learning_path(self, request: CareerCoachRequest) -> str:
        prompt = f"""
        당신은 수많은 개발자들의 이력서를 리뷰하고 커리어 성장을 성공적으로 이끈, 경험 많은 시니어 개발자이자 커리어 멘토입니다. 당신의 임무는 지원자의 이력서 내용을 면밀히 분석하여, 그의 강점과 약점을 진단하고, 성장을 위해 가장 필요한 부분에 대한 '맞춤형 액션 플랜'을 제안하는 것입니다.

        [지원자 정보]
        - 경력 요약: {request.careerSummary}
        - 수행 직무 및 프로젝트: {request.jobDuties}
        - 보유 기술 스킬: {", ".join(request.technicalSkills)}

        [지시사항]
        1. 심층 분석 및 진단: 먼저, 주어진 지원자 정보를 바탕으로 현재 기술 스택의 숙련도, 프로젝트 경험의 깊이, 성장 잠재력 등을 종합적으로 분석하고 진단해 주세요.
        2. 진단 기반의 동적 추천: 분석 결과에 따라, 아래 항목들 중 지원자에게 가장 필요하다고 판단되는 것들을 선별하여 구체적인 실행 방안을 제안해 주세요. 모든 항목을 포함할 필요는 없으며, 진단 결과에 따라 2~4개의 가장 중요한 추천을 구성합니다.
            * [기술 역량 심화]: 만약 특정 기술에 대한 숙련도가 더 필요하다고 판단되면, 해당 기술의 고급 주제나 내부 동작 원리에 대해 깊이 학습할 수 있는 구체적인 방법을 추천합니다. (예: 특정 공식 문서, 추천 도서, 심화 강의 등)
            * [기술 스택 확장]: 만약 현재 기술 스택이 특정 분야에 치우쳐 있거나, 시장 트렌드에 맞는 기술이 부족하다고 판단되면, 시너지를 낼 수 있는 새로운 기술이나 플랫폼을 추천합니다.
            * [프로젝트 경험 강화]: 만약 언급된 프로젝트 경험이 기술 스킬에 비해 부족하거나 특정 역량을 보여주기 어렵다고 판단되면, 부족한 부분을 채울 수 있는 구체적인 사이드 프로젝트 아이디어를 제안합니다. 프로젝트의 목표, 추천 기술 스택, 예상되는 결과물을 명확히 제시해야 합니다.
            * [커뮤니케이션 및 리더십 강화]: 만약 이력서 내용에서 기술 외적인 역량(예: 협업, 문제 해결 과정 공유, 리더십)에 대한 어필이 부족하다고 판단되면, 기술 블로그 작성, 오픈소스 기여, 세미나 발표 등 소프트 스킬을 강화하고 증명할 수 있는 구체적인 활동을 추천합니다.
        3. 구체성과 실행 가능성: 모든 추천은 추상적인 조언이 아닌, 당장 시작할 수 있을 만큼 구체적이고 실용적인 액션 아이템이어야 합니다.
        4. 출력 형식: 최종 결과물은 서론(간단한 진단평)과 본론(추천 항목들)으로 구성된 자연스러운 마크다운(Markdown) 텍스트 형식으로 작성해 주세요. 각 추천 항목은 명확한 제목을 가져야 합니다.

        이제 위 지시사항에 따라, 주어진 지원자 정보를 바탕으로 개인 맞춤형 학습 경로를 생성해 주세요.
        """
        try:
            # Google Gemini API 호출
            response = await asyncio.to_thread(
                model.generate_content,
                prompt
            )
            return response.text
        except Exception as e:
            print(f"Error generating learning path: {e}")
            return "AI 모델 호출 중 오류가 발생했습니다. API 키와 서버 상태를 확인해주세요."
