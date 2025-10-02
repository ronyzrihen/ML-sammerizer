from fastapi import FastAPI
from translator import Translator
from pydantic import BaseModel


app = FastAPI()
translator = Translator()

class TranslateRequest(BaseModel):
    text: str
    src_lang: str = "heb_Hebr"
    tgt_lang: str = "eng_Latn"

@app.get("/")
def healthcheck():
    return "translator is up and running"

@app.post("/translate")
def translate(req: TranslateRequest):
    print("Received translation request:", req)
    translation = translator.translate(req.text, req.src_lang, req.tgt_lang)
    return {"translation": translation}
