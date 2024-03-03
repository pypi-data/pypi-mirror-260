import string
import random

def generate_id(length=20):
    """
    Generates an alphanumeric password of a given length.
    
    Parameters:
    - length: int, the desired length of the password
    
    Returns:
    - str, the generated alphanumeric password
    """
    characters = string.ascii_letters  # Combine letters and digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
