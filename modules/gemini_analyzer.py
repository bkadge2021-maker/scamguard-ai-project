import json
from config import GEMINI_API_KEY, GEMINI_MODEL
from modules.schemas import ScamAnalysis
from modules.prompt_engineering import build_prompt
from modules.risk_scorer import score_signals

class GeminiConfigurationError(RuntimeError):
    pass

def analyze_with_gemini(message, prompt_mode="zero_shot", language="Auto / English", baseline=None):
    if not GEMINI_API_KEY:
        raise GeminiConfigurationError("Gemini API key not found. Copy .env.example to .env and add GEMINI_API_KEY.")
    from google import genai
    client=genai.Client(api_key=GEMINI_API_KEY)
    prompt=build_prompt(message, prompt_mode, language, baseline)
    response=client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={"response_mime_type":"application/json"}
    )
    raw=response.text or ""
    data=json.loads(raw)
    validated=ScamAnalysis.model_validate(data).model_dump()
    # Merge local, observable signals with validated LLM result for transparency.
    signals=(baseline or {}).get("signals", [])
    validated["signals"]=signals
    validated["verdict"]=f"{validated['classification']}: {validated['intent']}"
    validated["recommendations"] = validated["recommendations"] or (baseline or {}).get("recommendations", [])
    return validated
