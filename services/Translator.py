from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, TextIteratorStreamer
import torch, threading

from pydantic import BaseModel

class Translator:
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-moe-54b")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" 
        )   

    def translate(self, text, src_lang ="heb_Hebr"):

        self.tokenizer.src_lang = src_lang
        inputs = self.tokenizer(text, return_tensors="pt")
        inputs["forced_bos_token_id"] = self.tokenizer.convert_tokens_to_ids("eng_Latn")
        output_ids = self.model.generate(**inputs)
        translation = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return translation
    
    def stream_translation(self, text: str, tgt_lang="heb_Hebr"):
        formated_text = prepare_for_translation(text)
        self.tokenizer.src_lang = "eng_Latn"
        inputs = self.tokenizer(formated_text, return_tensors="pt")
        inputs["forced_bos_token_id"] = self.tokenizer.convert_tokens_to_ids(tgt_lang)
        
        streamer = TextIteratorStreamer(self.tokenizer, skip_special_tokens=True)
        for k in inputs:
           if isinstance(inputs[k], torch.Tensor):
               inputs[k] = inputs[k].to(self.model.device)
        
        gen_kwargs = dict(
            **inputs,
            do_sample=False,           
            streamer=streamer
        )   
        thread = threading.Thread(target=self.model.generate, kwargs=gen_kwargs)
        thread.start()
        
        for chunk in streamer:
            yield restore_formatting(chunk)

class TranslateRequest(BaseModel):
    text: str
    src_lang: str = "heb_Hebr"
    tgt_lang: str = "eng_Latn"
    stream: bool = False


def prepare_for_translation(input_text: str):
    text = input_text.replace("\n", "<NEW_LINE> ")
    return text

def restore_formatting(translated_text: str):
    text = translated_text.replace("<NEW_LINE>", "\n")
    return text
