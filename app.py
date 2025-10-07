from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from services.Translator import Translator
from services.Summerizer import Summerizer
from schemas.summerize import Language, SummerizeRequest

translator = Translator()
summerizer = Summerizer()

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


@app.post("/summerize")
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
    """
    Summarize a given text with the following workflow:

    1.  **Translate (if necessary):** The input text is translated to English for the summarization model.
    2.  **Summarize:** The English text is summarized.
    3.  **Translate Back (if necessary):** If the target language is not English, the summary is translated back to the target language.

    The response is always a stream.
    """
    if not req.text:
        return {"error": "Text is required"}
    print("Translating text...")
    translated_text = translator.translate_to_english(req.text, req.src_lang.value)
    print("translated_text:", translated_text)
    print("Summarizing text...")

    is_target_english = req.tgt_lang.value == Language.ENGLISH.value
    options = {"temperature": req.temperature, "top_p": req.top_p, "num_predict": req.max_tokens}
    summary_stream = summerizer.summarize(translated_text, options, stream=is_target_english)

    if is_target_english:
        return StreamingResponse(summary_stream, media_type="text/event-stream")

    translated_stream = translator.translate_from_english(
        text=summary_stream,
        tgt_lang=req.tgt_lang.value
    )
    return StreamingResponse(translated_stream, media_type="text/event-stream")
