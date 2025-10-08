import torch
from core.decorators import singleton
from config import NLLB_MODEL_NAME
from schemas import Language
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


@singleton
class Translator:

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(NLLB_MODEL_NAME)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            NLLB_MODEL_NAME,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto",
        )

    def translate(self, text: str, src_lang: str, tgt_lang: str):
        self.tokenizer.src_lang = src_lang
        inputs = self.tokenizer(text, return_tensors="pt")
        inputs["forced_bos_token_id"] = self.tokenizer.convert_tokens_to_ids(tgt_lang)
        output_ids = self.model.generate(**inputs)
        res = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return res

    def translate_to_english(self, text, src_lang=Language.HEBREW.value):
        return self.translate(text, src_lang, Language.ENGLISH.value)

    def translate_from_english(self, text, tgt_lang):
        return self.translate(text, Language.ENGLISH.value, tgt_lang)
