from transformers import pipeline

from pydantic import BaseModel

class Translator:
    def __init__(self):
        self.pipe = pipeline("translation", model="facebook/nllb-200-distilled-600M")

    def translate(self, text, src_lang ="heb_Hebr", tgt_lang="eng_Latn"):
        res = self.pipe(
            text,
            src_lang=src_lang,
            tgt_lang=tgt_lang,
        )
        return res[0]['translation_text']
    
class TranslateRequest(BaseModel):
    text: str
    src_lang: str = "heb_Hebr"
    tgt_lang: str = "eng_Latn"

