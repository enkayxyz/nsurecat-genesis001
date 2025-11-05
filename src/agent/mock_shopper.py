import time
import os
import random
from typing import Dict, Any

# Try to import OpenAI, but fall back to mock if not available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Insurance carriers for realistic responses
CARRIERS = [
    "Rebel Mutual", "Liberty Shield", "Progressive Plus",
    "State Trust", "All-Guard Insurance", "Nationwide Protect",
    "SafeDrive Insurance", "Guardian Auto", "First Rate Insurance"
]

def find_savings(data: Dict[str, Any]) -> Dict[str, float]:
    """
    AI agent that shops for insurance quotes.

    Uses OpenAI if OPENAI_API_KEY is set, otherwise uses smart mock logic.

    Args:
        data: Policy details including coverage amounts

    Returns:
        dict with savings_6mo (float) and new_carrier (str)
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if openai_api_key and OPENAI_AVAILABLE:
        return _find_savings_with_ai(data, openai_api_key)
    else:
        return _find_savings_mock(data)


def _find_savings_with_ai(data: Dict[str, Any], api_key: str) -> Dict[str, float]:
    """Use OpenAI to generate realistic insurance quotes"""

    time.sleep(1)  # Simulate API call time

    try:
        client = OpenAI(api_key=api_key)

        # Build prompt with policy details
        prompt = f"""You are an insurance shopping AI agent. Based on the following policy details,
suggest a competitive 6-month savings amount and a realistic insurance carrier name.

Policy Details:
- Bodily Injury: {data.get('bodily_injury', 'N/A')}
- Property Damage: {data.get('property_damage', 'N/A')}
- Uninsured Motorist: {data.get('uninsured_motorist', 'N/A')}
- Collision Deductible: {data.get('collision', 'N/A')}
- Comprehensive Deductible: {data.get('comprehensive', 'N/A')}
- Personal Injury Protection: {data.get('personal_injury_protection', 'N/A')}

Respond ONLY with a JSON object in this exact format (no markdown, no explanation):
{{"savings_6mo": <amount>, "new_carrier": "<carrier name>"}}

Make the savings realistic (between $150-$400 for 6 months) and use a real-sounding carrier name."""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful insurance shopping assistant that returns JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100
        )

        # Parse response
        result_text = response.choices[0].message.content.strip()

        # Try to extract JSON (handle markdown code blocks)
        if "```" in result_text:
            result_text = result_text.split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]

        import json
        result = json.loads(result_text)

        return {
            "savings_6mo": float(result.get("savings_6mo", 246.0)),
            "new_carrier": result.get("new_carrier", "Progressive Plus")
        }

    except Exception as e:
        # Fall back to mock if OpenAI fails
        print(f"OpenAI API error: {e}. Falling back to mock.")
        return _find_savings_mock(data)


def _find_savings_mock(data: Dict[str, Any]) -> Dict[str, float]:
    """
    Smart mock agent that varies responses based on coverage details.
    More realistic than pure hardcoded values.
    """
    time.sleep(2)  # Simulate processing time

    # Calculate base savings based on coverage amounts
    base_savings = 150.0

    # Extract coverage info and calculate risk-adjusted savings
    try:
        # Higher coverage limits = more potential savings
        bodily_injury = data.get('bodily_injury', '100000/300000')
        if '300000' in str(bodily_injury) or '500000' in str(bodily_injury):
            base_savings += 50

        # Lower deductibles = higher premium = more savings potential
        collision = str(data.get('collision', '1000'))
        if '500' in collision or collision == '500':
            base_savings += 40
        elif '1000' in collision:
            base_savings += 20

        comprehensive = str(data.get('comprehensive', '500'))
        if '500' in comprehensive or comprehensive == '500':
            base_savings += 30
        elif '1000' in comprehensive:
            base_savings += 15

        # Uninsured motorist coverage adds savings potential
        uninsured = data.get('uninsured_motorist', '')
        if uninsured:
            base_savings += 25

        # PIP coverage increases savings potential
        pip = str(data.get('personal_injury_protection', ''))
        if pip and pip != '0':
            base_savings += 30

    except Exception:
        # If parsing fails, use default base
        pass

    # Add some randomness for realism (±10%)
    variation = random.uniform(0.9, 1.1)
    final_savings = round(base_savings * variation, 2)

    # Ensure reasonable range
    final_savings = max(150.0, min(400.0, final_savings))

    # Pick a random carrier
    carrier = random.choice(CARRIERS)

    return {
        "savings_6mo": final_savings,
        "new_carrier": carrier
    }


# Backward compatibility
def find_savings_simple() -> Dict[str, float]:
    """Simple version for testing - always returns same result"""
    return {
        "savings_6mo": 246.00,
        "new_carrier": "Rebel Mutual"
    }
