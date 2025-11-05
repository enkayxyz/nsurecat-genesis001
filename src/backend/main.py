# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import StreamingResponse
# from pydantic import BaseModel
# import httpx
# import os

# # Import routers
# from api_routes.shop import router as shop_router
# from api_routes.save import router as save_router

# app = FastAPI()

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include routers
# app.include_router(shop_router, prefix="/v1", tags=["shop"])
# app.include_router(save_router, prefix="/v1", tags=["save"])

# # ElevenLabs configuration
# ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
# VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Default voice (Rachel)

# class TextToSpeechRequest(BaseModel):
#     text: str
#     voice_id: str = VOICE_ID

# @app.post("/api/text-to-speech")
# async def text_to_speech(request: TextToSpeechRequest):
#     """Convert text to speech using ElevenLabs API"""
    
#     url = f"https://api.elevenlabs.io/v1/text-to-speech/{request.voice_id}"
    
#     headers = {
#         "Accept": "audio/mpeg",
#         "Content-Type": "application/json",
#         "xi-api-key": ELEVENLABS_API_KEY
#     }
    
#     data = {
#         "text": request.text,
#         "model_id": "eleven_monolingual_v1",
#         "voice_settings": {
#             "stability": 0.5,
#             "similarity_boost": 0.5
#         }
#     }
    
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.post(url, json=data, headers=headers, timeout=30.0)
            
#             if response.status_code != 200:
#                 raise HTTPException(
#                     status_code=response.status_code,
#                     detail=f"ElevenLabs API error: {response.text}"
#                 )
            
#             return StreamingResponse(
#                 iter([response.content]),
#                 media_type="audio/mpeg",
#                 headers={
#                     "Content-Disposition": "inline; filename=speech.mp3"
#                 }
#             )
#     except httpx.TimeoutException:
#         raise HTTPException(status_code=504, detail="Request to ElevenLabs timed out")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/voices")
# async def get_voices():
#     """Get available voices from ElevenLabs"""
    
#     url = "https://api.elevenlabs.io/v1/voices"
#     headers = {"xi-api-key": ELEVENLABS_API_KEY}
    
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(url, headers=headers)
            
#             if response.status_code != 200:
#                 raise HTTPException(
#                     status_code=response.status_code,
#                     detail="Failed to fetch voices"
#                 )
            
#             return response.json()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI
from backend.app.wallet_sets import create_wallet_set
from backend.app.wallets import create_wallet, get_wallet_balance
from backend.app.transfers import transfer_tokens
from backend.app.getTransactionState import transaction_status
from pydantic import BaseModel
app = FastAPI(title="Circle Wallet Backend")

@app.get("/")
def root():
    return {"message": "Circle Wallet Backend Running 🚀"}

@app.post("/wallet-sets/create")
def create_wallet_set_endpoint(name: str):
    return create_wallet_set(name)

@app.post("/wallets/create")
def create_wallet_endpoint():
    return create_wallet()

@app.get("/wallets/balance/{wallet_id}")
def get_balance(wallet_id: str):
    return get_wallet_balance(wallet_id)

class TransferRequest(BaseModel):
    source_wallet_id: str
    destination_wallet_id: str
    amount: str
    token_address: str

@app.post("/transfers")
def transfer_tokens_endpoint(request: TransferRequest):
    return transfer_tokens(
        request.source_wallet_id,
        request.destination_wallet_id,
        request.amount,
        request.token_address
    )

@app.get("/transactions/{transaction_id}")
def get_transaction_status(transaction_id: str):
    return transaction_status(transaction_id)