# strands/__init__.py
from .models.echo import EchoModel

class Agent:
    def __init__(self):
        self.model = EchoModel()
    
    def run(self, text: str):
        return self.model.predict(text)
