import json
from requests import post
from .helper import BaseProvider

class DeepInfra(BaseProvider):
    url = "https://deepinfra.com"
    api = "https://api.deepinfra.com"

    models = [
        "meta-llama/Llama-2-70b-chat-hf",
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "meta-llama/Llama-2-13b-chat-hf",
        "meta-llama/Llama-2-7b-chat-hf",
        "codellama/CodeLlama-34b-Instruct-hf",
        "codellama/CodeLlama-70b-Instruct-hf",
        "deepinfra/airoboros-70b",
        "mistralai/Mistral-7B-Instruct-v0.1",
        "lizpreciatior/lzlv_70b_fp16_hf",
        "openchat/openchat_3.5",
        "Phind/Phind-CodeLlama-34B-v2",
        "amazon/MistralLite",
        "cognitivecomputations/dolphin-2.6-mixtral-8x7b",
        "01-ai/Yi-34B-Chat",
    ]
    default_model = models[0]

    @classmethod
    def create_response(cls, model: str = "", messages: list = []):
        if model is None: model = cls.default_provider
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
            "Accept": "text/event-stream",
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
            "model": model,
            "messages": messages,
            "stream": True
        }

        res = post(
            url = f"{cls.api}/v1/openai/chat/completions",
            json = data,
            headers = headers
        )

        res.raise_for_status()
        first = True
        for chunk in res.iter_lines():
            if not chunk.startswith(b"data: "):
                continue
            try:
                json_line = json.loads(chunk[6:])
                choices = json_line.get("choices", [{}])

                if choices[0].get("finish_reason"):
                    break
                token = choices[0].get("delta", {}).get("content")
                if token:
                    if first:
                        token = token.lstrip()
                    if token:
                        first = False
                        yield token
            except:
                pass

    @staticmethod
    def get_models():
        raise Exception("A provider need a 'get_models' function.")