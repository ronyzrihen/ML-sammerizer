from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, TextIteratorStreamer
from schemas.summerize import Language
import torch
import threading
from core import singleton
from config import NLLB_MODEL_NAME


@singleton
class Translator:
    NEWLINE_INDICATOR = "<NEW_LINE>"

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(NLLB_MODEL_NAME)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            NLLB_MODEL_NAME,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto",
        )

    def translate_to_english(self, text, src_lang=Language.HEBREW.value):
        self.tokenizer.src_lang = src_lang
        inputs = self.tokenizer(text, return_tensors="pt")
        inputs["forced_bos_token_id"] = self.tokenizer.convert_tokens_to_ids(Language.ENGLISH.value)
        output_ids = self.model.generate(**inputs)
        translation = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return translation

    def translate_from_english(self, text: str, tgt_lang=Language.HEBREW.value):
        self.tokenizer.src_lang = Language.ENGLISH.value
        encoded_text = text.replace("\n", self.NEWLINE_INDICATOR)
        print("encoded_text: ", encoded_text)
        inputs = self.tokenizer(encoded_text, return_tensors="pt")
        inputs["forced_bos_token_id"] = self.tokenizer.convert_tokens_to_ids(tgt_lang)

        streamer = TextIteratorStreamer(self.tokenizer, skip_special_tokens=True)
        for k in inputs:
            if isinstance(inputs[k], torch.Tensor):
                inputs[k] = inputs[k].to(self.model.device)

        gen_kwargs = dict(**inputs, do_sample=False, streamer=streamer)
        thread = threading.Thread(target=self.model.generate, kwargs=gen_kwargs)
        thread.start()

        for chunk in streamer:
            text = chunk.replace(self.NEWLINE_INDICATOR, "\n")
            print("chunck: ", chunk)
            print("recoded: ", text)
            yield text
