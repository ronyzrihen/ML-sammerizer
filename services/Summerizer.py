from requests import post
import json
import httpx
from core import singleton
from config import PHI_MODEL_NAME, OLLAMA_API_URL
from services.Translator import Translator
from schemas import Language


@singleton
class Summerizer:
    def __init__(self, translator: Translator):
        self.translator = translator
        self.api_url = OLLAMA_API_URL
        self.model_name = PHI_MODEL_NAME

    def summarize(self, text: str, options: dict = {}, tgt_lang: str = Language.HEBREW.value):
        prompt = f"Summarize the following text into exactly 5 concise bullet points:\n\n{text}"

        data = {
            "model": self.model_name,
            "prompt": prompt,
            "options": options,
            "stream": True,
        }

        def generate():
            with httpx.stream("POST", f"{self.api_url}/api/generate", json=data, timeout=None) as response:
                if response.status_code != 200:
                    raise Exception(f"Ollama error {response.status_code}: {response.text}")

                buffer = ""
                for chunck in response.iter_lines():
                    if not chunck:
                        continue
                    try:
                        json_line = json.loads(chunck)
                        if "response" in json_line:
                            buffer += json_line["response"]
                        if "\n" in buffer:
                            line, buffer = buffer.split("\n", 1)
                            if not line:
                                continue
                            yield self.translator.translate_from_english(line, tgt_lang) + "\n"
                    except json.JSONDecodeError:
                        continue
                if buffer.strip():
                    yield self.translator.translate_from_english(buffer, tgt_lang)

        return generate()
