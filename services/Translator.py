from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from pydantic import BaseModel

class Translator:
    def __init__(self, model_name: str):
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def translate(self, text, src_lang ="heb_Hebr", tgt_lang="eng_Latn"):

        self.tokenizer.src_lang = src_lang
        inputs = self.tokenizer(text, return_tensors="pt")
        output_ids = self.model.generate(**inputs)
        translation = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return translation
    
    def stream_translation(self, text: str, src_lang="eng_Latn", tgt_lang="heb_Hebr"):
        self.tokenizer.src_lang = src_lang
        inputs = self.tokenizer(text, return_tensors="pt")

        if hasattr(self.tokenizer, "lang_code_to_id"):
            forced_bos_token_id = self.tokenizer.lang_code_to_id[tgt_lang]
        else:
            forced_bos_token_id = self.tokenizer.convert_tokens_to_ids(tgt_lang)
        generated = inputs["input_ids"]

        for _ in range(512):
            outputs = self.model.generate(
                generated,
                forced_bos_token_id=forced_bos_token_id,
                max_new_tokens=1,
                do_sample=False
            )
            new_token = outputs[0, -1].unsqueeze(0)
            generated = torch.cat((generated, new_token.unsqueeze(0)), dim=1)

            decoded = self.tokenizer.decode(
                generated[0],
                skip_special_tokens=True,
                clean_up_tokenization_spaces=True
            )
            yield decoded + "\n"
class TranslateRequest(BaseModel):
    text: str
    src_lang: str = "heb_Hebr"
    tgt_lang: str = "eng_Latn"
    return_src: bool = True
    stream: bool = False

