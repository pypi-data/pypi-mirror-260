from rich.console import Console
import time
import random


console = Console()
delay_options = [0.0001, 0.0002, 0.0003, 0.01, 0.01, 0.1]

def stream_message(message, speed=1):
    for char in message:
        delay = random.choice(delay_options) / speed
        console.print(char, end="", style="bold")
        time.sleep(delay)
    console.print() 