import os
from fastapi import FastAPI
from services.Translator import Translator, TranslateRequest
from services.Sammerizer import Summerizer


app_state = {}

async def lifespan(app: FastAPI):
    ollama_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
    model_name = os.getenv("MODEL_NAME", "rouge/phi-3.5-mini-4k-instruct")
    app_state["summerizer"] = Summerizer(ollama_url, model_name)
    app_state["translator"] = Translator()
    yield
    app_state.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def healthcheck():
    return "translator is up and running"

@app.post("/translate")
def get_translatation(req: TranslateRequest):
    if not req.text:
        return {"error": "Text is required"}
    return translate(req.text, req.src_lang, req.tgt_lang)

@app.post("/summerize")
def summerize(req: TranslateRequest):
    if not req.text:
        return {"error": "Text is required"}
    print("Translating text...")
    translated_text = translate(req.text, req.src_lang, req.tgt_lang)
    print("translated_text:", translated_text)
    print("Summarizing text...")
    return app_state["summerizer"].summerize(translated_text)

def translate(text: str, src_lang ="heb_Hebr", tgt_lang ="eng_Latn") -> str:
    translator = app_state.get("translator")
    translation = translator.translate(text, src_lang, tgt_lang)
    return translation
    
