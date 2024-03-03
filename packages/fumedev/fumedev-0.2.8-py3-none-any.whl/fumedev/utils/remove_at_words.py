import re

def remove_at_words(text):
    # Pattern to match words that start with @
    pattern = r'@\w+'
    # Replace these words with an empty string
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text