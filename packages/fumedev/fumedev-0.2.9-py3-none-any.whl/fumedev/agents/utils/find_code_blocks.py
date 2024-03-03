import re

def find_code_blocks(text):

    priority = find_js_blocks(text) + find_python_blocks(text) + find_plaintext_blocks(text) + find_diff_blocks(text)

    if not priority:
        return find_undefined_blocks(text)

    return priority

def find_js_blocks(text):
    # Regular expression pattern
    # This will match triple backticks followed by 'javascript', and then capture everything (including newlines) until the next triple backticks
    pattern = r"```javascript(.*?)```"

    # Finding all matches with the re.DOTALL flag to include newlines
    matches = re.findall(pattern, text, re.DOTALL)

    return matches

def find_python_blocks(text):
    # Regular expression pattern
    # This will match triple backticks followed by 'javascript', and then capture everything (including newlines) until the next triple backticks
    pattern = r"```python(.*?)```"

    # Finding all matches with the re.DOTALL flag to include newlines
    matches = re.findall(pattern, text, re.DOTALL)

    return matches

def find_plaintext_blocks(text):
    # Regular expression pattern
    # This will match triple backticks followed by 'javascript', and then capture everything (including newlines) until the next triple backticks
    pattern = r"```plaintext(.*?)```"

    # Finding all matches with the re.DOTALL flag to include newlines
    matches = re.findall(pattern, text, re.DOTALL)

    return matches

def find_diff_blocks(text):
    # Regular expression pattern
    # This will match triple backticks followed by 'javascript', and then capture everything (including newlines) until the next triple backticks
    pattern = r"```diff(.*?)```"

    # Finding all matches with the re.DOTALL flag to include newlines
    matches = re.findall(pattern, text, re.DOTALL)

    return matches

def find_undefined_blocks(text):
    # Regular expression pattern
    # This will match triple backticks followed by 'javascript', and then capture everything (including newlines) until the next triple backticks
    pattern = r"```(.*?)```"

    # Finding all matches with the re.DOTALL flag to include newlines
    matches = re.findall(pattern, text, re.DOTALL)

    return matches