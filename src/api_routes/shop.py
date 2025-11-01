from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.agent.mock_shopper import find_savings

router = APIRouter()

class ShopRequest(BaseModel):
    # Define Key 6 fields - placeholder, adjust as per requirements
    bodily_injury: str
    property_damage: str
    uninsured_motorist: str
    collision: str
    comprehensive: str
    personal_injury_protection: str

@router.post("/shop")
async def shop(request: ShopRequest):
    try:
        # Call the AI agent
        savings = find_savings(request.dict())
        return savings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))