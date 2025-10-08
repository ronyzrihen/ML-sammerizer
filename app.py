from fastapi import FastAPI, Body
from services.Translator import Translator
from services.Summerizer import Summerizer
from fastapi.responses import StreamingResponse
from schemas.summerize import SummerizeRequest
from schemas.translate import TranslateRequest

translator = Translator()
summerizer = Summerizer(translator)

app = FastAPI(
    title="AI Summarizer API",
    description="An API to summarize text, with optional translation.",
    version="1.0.0",
)


@app.get("/healthcheck")
def healthcheck():
    """
    Check if the API is up and running.
    """
    return "Summerizer is up and running"


@app.post(
    "/translate",
    summary="Translate text between languages",
    description=(
        "Translates the given text from the source language (`src_lang`) "
        "to the target language (`tgt_lang`) using the NLLB translation model. "
        "Supports ISO-like language codes such as `eng_Latn` for English and `heb_Hebr` for Hebrew."
    ),
)
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
    return {
        "translation": translator.translate(req.text, req.src_lang.value, req.tgt_lang.value)
    }


@app.post(
    "/summerize",
    summary="Summarize a given text",
    description="""
Summarize a given text using a multi-step workflow:

1. **Translate (if necessary):** The input text is translated to English for the summarization model.
2. **Summarize:** The English text is summarized.
3. **Translate Back (if necessary):** If the target language is not English, the summary is translated back to the target language.

The response is returned as a **text/event-stream** for real-time updates.
"""
)
def summerize(
    req: SummerizeRequest = Body(
        ...,
        example={
            "text": "טקסט ארוך בעברית שדורש סיכום... החלל הוא מקום עצום ומסתורי, מלא בכוכבים, גלקסיות ותופעות קוסמיות שטרם הבנו. האנושות תמיד שאפה לחקור אותו.",
            "src_lang": "heb_Hebr",
            "tgt_lang": "eng_Latn",
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 256
        },
    )
):
    if not req.text:
        return {"error": "Text is required"}
    translated_text = translator.translate_to_english(req.text, req.src_lang.value)
    options = {"temperature": req.temperature, "top_p": req.top_p, "num_predict": req.max_tokens}
    summary_stream = summerizer.summarize(translated_text, options, req.tgt_lang.value)

    return StreamingResponse(summary_stream, media_type="text/event-stream")
