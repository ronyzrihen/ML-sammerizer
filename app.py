from fastapi import FastAPI
from Translator import Translator, TranslateRequest


app = FastAPI()
translator = Translator()

@app.get("/")
def healthcheck():
    return "translator is up and running"

@app.post("/translate")
def translate(req: TranslateRequest):
    if not req.text:
        return {"error": "Text is required"}
    print("Received translation request:", req)
    translation = translator.translate(req.text, req.src_lang, req.tgt_lang)
    return {"translation": translation}
