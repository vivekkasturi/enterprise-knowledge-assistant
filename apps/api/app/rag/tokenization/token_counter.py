import tiktoken


class TokenCounter:
    def __init__(self):
        self.tokenizer = tiktoken.get_encoding("o200k_harmony")

    def count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))
