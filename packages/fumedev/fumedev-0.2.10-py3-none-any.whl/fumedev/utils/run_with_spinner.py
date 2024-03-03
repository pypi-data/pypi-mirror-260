from queue import Queue
from rich.console import Console
from threading import Thread
import time

console = Console()

def run_with_spinner(function, message, *args, **kwargs):
    # Create a queue to hold the result
    result_queue = Queue()

    # Define a wrapper function to call the original function and store its result in the queue
    def wrapper_func(*args, **kwargs):
        result = function(*args, **kwargs)
        result_queue.put(result)

    with console.status(message, spinner="dots") as status:
        # Use the wrapper function instead of the original function
        thread = Thread(target=wrapper_func, args=args, kwargs=kwargs)
        thread.start()

        while thread.is_alive():
            time.sleep(0.1)
    
    # Return the result from the queue
    return result_queue.get()