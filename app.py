from core.logger import logger
from core.decorators import handle_errors
from services.Translator import Translator
from services.Summerizer import Summerizer
from schemas.summerize import SummerizeRequest
from schemas.translate import TranslateRequest
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Body, HTTPException

translator = Translator()
summerizer = Summerizer(translator)

app = FastAPI(
    title="AI Summarizer API",
    description="An API to summarize text, with optional translation.",
)


@app.get("/healthcheck")
@handle_errors
def healthcheck():
    """
    Check if the API is up and running.
    """
    logger.info("Healthcheck endpoint was called.")
    return "Summerizer is up and running"


@app.post(
    "/translate",
    summary="Translate text between languages",
    description=(
        "Translates the given text from the source language (`src_lang`) "
        "to the target language (`tgt_lang`) using the NLLB translation model."
    ),
)
@handle_errors
def translate(
    req: TranslateRequest = Body(
        ...,
        example={
            "text": "Hello, how are you?",
            "src_lang": "eng_Latn",
            "tgt_lang": "heb_Hebr"
        },
    )
):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Text field cannot be empty.")
    
    logger.info(f"Translating text from {req.src_lang.value} to {req.tgt_lang.value}")
    translation_result = translator.translate(req.text, req.src_lang.value, req.tgt_lang.value)
    return {
        "translation": translation_result
    }


@app.post(
    "/summarize",
    description="""
Summarize a given text using a multi-step workflow:

1. **Translate (if necessary):** The input text is translated to English for the summarization model.
2. **Summarize:** The English text is summarized.
3. **Translate Back (if necessary):** If the target language is not English, the summary is translated back to the target language.

The response is returned as a **text/event-stream** for real-time updates.
"""
)
@handle_errors
def summarize(
    req: SummerizeRequest = Body(
        ...,
        example={
            "text": """
            אניגמה היא משפחה של מכונות להצפנה ולפענוח של מסרים טקסטואליים,
            ששימשו את הכוחות הגרמנים והאיטלקים במלחמת העולם השנייה. בזכות התקשורת המוצפנת שאפשרה האניגמה,
            הצליח הקריגסמרינה (הצי הגרמני), ובמיוחד צי הצוללות, במהלך המערכה באוקיינוס האטלנטי (1939–1945),
            להטיל מצור אפקטיבי על בריטניה, מצור שמנע אספקת מזון ואמצעי לחימה לאי הבריטי, בדרך הים.
            """,
            "src_lang": "heb_Hebr",
            "tgt_lang": "heb_Hebr",
            "temperature": 0.7, "top_p": 0.9, "max_tokens": 256
        },
    )
):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Text field cannot be empty.")

    logger.info(f"Summarizing text from {req.src_lang.value} to {req.tgt_lang.value}")
    translated_text = translator.translate_to_english(req.text, req.src_lang.value)
    options = {"temperature": req.temperature, "top_p": req.top_p, "num_predict": req.max_tokens}
    summary_stream = summerizer.summarize(translated_text, options, req.tgt_lang.value)

    return StreamingResponse(summary_stream, media_type="text/event-stream")
