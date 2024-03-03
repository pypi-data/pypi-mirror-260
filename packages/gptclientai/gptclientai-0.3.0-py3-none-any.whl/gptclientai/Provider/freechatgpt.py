from requests import post
from .helper import BaseProvider

class FreeChatGpt(BaseProvider):
    url = "https://free.chatgpt.org.uk"

    models = [
        "google-gemini-pro"
    ]
    default_model = models[0]

    @classmethod
    def create_response(cls, model: str = "", messages: list = []):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Accept": "application/json",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": f"{cls.url}/chat",
            "Content-Type": "application/json",
            "Flag-Real-Time-Data": "false",
            "Origin": cls.url,
            "Alt-Used": "koala.sh",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

        data = {
            "messages": messages,
            "model": cls.default_model,
            "temperature": 0.5,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "top_p": 1,
            "max_tokens": None
        }

        res = post(
            url = f"{cls.url}/api/openai/v1/chat/completions",
            json = data,
            headers = headers
        )

        return res.json()["choices"][0]["message"]["content"]
    
    @staticmethod
    def get_models():
        raise Exception("A provider need a 'get_models' function.")