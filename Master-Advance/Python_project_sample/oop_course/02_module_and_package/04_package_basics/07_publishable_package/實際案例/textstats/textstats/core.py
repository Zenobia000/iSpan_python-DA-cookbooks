from collections import Counter

def count_chars(text: str) -> int:
    return len(text)

def count_words(text: str) -> int:
    return len(text.split())

def most_common_words(text: str, n: int = 3):
    words = text.lower().split()
    return Counter(words).most_common(n)
