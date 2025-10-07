import os
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from services.Translator import Translator, TranslateRequest
from services.Sammerizer import Summerizer


app_state = {}

async def lifespan(app: FastAPI):
    ollama_url = os.getenv("OLLAMA_API_URL")
    phi_model_name = os.getenv("PHI_MODEL_NAME")
    nllb_model_name = os.getenv("NLLB_MODEL_NAME")
    app_state["summerizer"] = Summerizer(ollama_url, phi_model_name)
    app_state["translator"] = Translator(nllb_model_name)
    yield
    app_state.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/healthcheck")
def healthcheck():
    return "Summerizer is up and running"

@app.post("/translate")
def get_translatation(req: TranslateRequest):
    translator = app_state.get("translator")
    if not req.text:
        return {"error": "Text is required"}
    if req.stream:
        streamed_translation = translator.stream_translation(
            text=req.text,
            src_lang=req.src_lang,
            tgt_lang=req.tgt_lang
        )
        return StreamingResponse(streamed_translation, media_type="text/event-stream")
    return translate(req.text, req.src_lang, req.tgt_lang)

@app.post("/summerize")
def summerize(req: TranslateRequest):
    if not req.text:
        return {"error": "Text is required"}
    print("Translating text...")
    translated_text = translate(req.text, req.src_lang, req.tgt_lang)
    print("translated_text:", translated_text)
    print("Summarizing text...")
    summerize = app_state["summerizer"].summerize(translated_text, req.stream)
    print("summ", summerize)
    if req.stream:
        return StreamingResponse(summerize, media_type="text/event-stream")
    return summerize

def translate(text: str, src_lang ="heb_Hebr", tgt_lang ="eng_Latn") -> str:
    translator = app_state.get("translator")
    translation = translator.translate(text, src_lang, tgt_lang)
    return translation
    
