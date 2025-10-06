from requests import post
import json

class Summerizer:
    def __init__(self, api_url: str, model_name: str):
        self.api_url = api_url
        self.model_name = model_name

    def summerize(self, text: str, stream: bool = False): 
        prompt = f"Summarize the following text into exactly 5 concise bullet points:\n\n{text}"

        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": stream
        }

        if stream:
            def generate():
                with post(f"{self.api_url}/api/generate", json=data, stream=True) as response:
                    if not response.ok:
                        raise Exception(f"Ollama error {response.status_code}: {response.text}")

                    for line in response.iter_lines():
                        if line:
                            try:
                                json_line = json.loads(line.decode("utf-8"))
                                if "response" in json_line:
                                    yield json_line["response"]
                            except json.JSONDecodeError:
                                continue
            return generate()
        
        else:
            response = post(f"{self.api_url}/api/generate", json=data, stream=False)
            response_json = response.json()
            print("Ollama response:", response_json.get("response"))
            
            if response.ok:
                return response_json.get("response")
            raise Exception(f"Ollama error {response.status_code}: {response.text}")
