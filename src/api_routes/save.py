from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.arc_service import process_fee

router = APIRouter()

class SaveRequest(BaseModel):
    wallet_address: str

@router.post("/save")
async def save(request: SaveRequest):
    try:
        # Call the Arc service
        result = process_fee(request.wallet_address)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))