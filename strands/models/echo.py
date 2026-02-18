# strands/models/echo.py
class EchoModel:
    def predict(self, text: str) -> str:
        # Just echo back the input text
        return f"Echo: {text}"
