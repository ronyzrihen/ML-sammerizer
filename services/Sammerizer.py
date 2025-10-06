from requests import post

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
            with post(f"{self.api_url}/api/generate", json=data) as response:
                if not response.ok:
                    raise Exception(f"Ollama error {response.status_code}: {response.text}")
                for line in response.iter_lines():
                    if line:
                        yield line.decode("utf-8")
        else:
            response = post(f"{self.api_url}/api/generate", json=data)
            print("Ollama response:", response.json())
            
            if response.ok:
                return response.json()
            raise Exception(f"Ollama error {response.status_code}: {response.text}")
