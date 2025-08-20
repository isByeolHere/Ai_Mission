from fastapi import APIRouter, Depends
from app.schemas.coach import CareerCoachRequest, CareerCoachResponse
from app.services.career_coach import CareerCoachService

router = APIRouter()

def get_career_coach_service() -> CareerCoachService:
    # This dependency injection allows for easier testing and management
    return CareerCoachService()

@router.post("/", response_model=CareerCoachResponse)
async def get_career_coaching(
    request: CareerCoachRequest,
    service: CareerCoachService = Depends(get_career_coach_service)
):
    """
    Receives user's career information and provides personalized interview questions and a learning path using an AI model.
    """
    return await service.get_coaching_advice(request)
