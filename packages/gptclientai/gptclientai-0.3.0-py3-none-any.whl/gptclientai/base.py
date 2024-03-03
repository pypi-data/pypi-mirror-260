
class BaseProvider:
    """
    Class for provider
    """

    @classmethod
    def create_response(cls, model: str = [], messages: list = []):
        raise Exception("A provider need a 'create_response' function.")
    
    @staticmethod
    def get_models():
        raise Exception("A provider need a 'get_models' function.")