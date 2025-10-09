import json
import httpx
from schemas import Language
from core.logger import logger
from core.decorators import singleton
from services.Translator import Translator
from config import PHI_MODEL_NAME, OLLAMA_API_URL


@singleton
class Summerizer:
    def __init__(self, translator: Translator):
        self.translator = translator
        self.api_url = OLLAMA_API_URL
        self.model_name = PHI_MODEL_NAME

    def summarize(self, text: str, options: dict = {}, tgt_lang: str = Language.HEBREW.value):
        
        prompt = f"""
        Summarize the following text. Provide exactly 5 short, numbered bullet points.
        - Number the bullets 1, 2, 3, 4, 5.
        - Use only the information from the text.
        - Do not add any extra information or explanations.
        Text to summarize:
        {text}
        Summary:
        """

        data = {
            "model": self.model_name,
            "prompt": prompt,
            "options": options,
            "stream": True,
        }

        def generate():
            try:
                with httpx.stream("POST", f"{self.api_url}/api/generate", json=data, timeout=None) as response:
                    if response.status_code != 200:
                        raise Exception(f"Ollama error {response.status_code}: {response.text}")

                    buffer = ""
                    for chunk in response.iter_lines():
                        if not chunk:
                            continue
                        try:
                            json_line = json.loads(chunk)
                            if "response" in json_line:
                                buffer += json_line["response"]
                            if "\n" in buffer:
                                line, buffer = buffer.split("\n", 1)
                                if not line:
                                    continue
                                yield self.translator.translate_from_english(line, tgt_lang) + "\n"
                        except json.JSONDecodeError:
                            logger.warning(f"Could not decode JSON line from Ollama stream: {chunk}")
                            continue
                    if buffer.strip():
                        yield self.translator.translate_from_english(buffer, tgt_lang)

            except httpx.HTTPStatusError as e:
                logger.error(f"Ollama API returned a non-200 status: {e.response.status_code} - {e.response.text}", exc_info=True)
                raise Exception(f"Failed to get response from summarization model: {e.response.status_code}") from e
            except httpx.RequestError as e:
                logger.error(f"Could not connect to Ollama API at {self.api_url}: {e}", exc_info=True)
                raise Exception("Could not connect to the summarization service.") from e

        return generate()
