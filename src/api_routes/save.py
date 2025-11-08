from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.arc_service import process_fee

router = APIRouter()

class SaveRequest(BaseModel):
    wallet_address: str
    fee_amount: int  # Amount in USDC smallest units (6 decimals)

@router.post("/save")
async def save(request: SaveRequest):
    try:
        # Call the Arc service with fee amount
        result = process_fee(request.wallet_address, request.fee_amount)
        return result  # Return the transaction data for frontend signing
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))