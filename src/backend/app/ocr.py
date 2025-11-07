# aiml_api.py
import os
import json
import requests
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

AIML_API_KEY = os.getenv("AIMLAPI_KEY")
AIML_URL = "https://api.aimlapi.com/v1/ocr"


def extract_text_from_document(document_url: str, doc_type: str = "document_url"):
    """Send document to AIML OCR API and get extracted text"""
    headers = {
        "Authorization": f"Bearer {AIML_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "mistral/mistral-ocr-latest",
        "document": {
            "type": doc_type,  # can be document_url or base64 if needed
            "document_url": document_url
        },
    }

    try:
        response = requests.post(AIML_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
