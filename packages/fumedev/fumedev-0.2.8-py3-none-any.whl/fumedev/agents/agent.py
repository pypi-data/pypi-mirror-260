import os

class Agent:
    """
    Represents an agent that tracks token count and handles project summaries.

    Attributes:
        total_tokens (int): The total number of tokens used by this agent.
        messages (list): A list of messages processed by the agent.
        project_summary (str): A summary of the project, loaded from a markdown file if available.
    """
    def __init__(self) -> None:
        """
        Initializes the Agent instance with default values.
        Attempts to load the project summary from a markdown file if it exists.
        """
        self.total_tokens = 0
        self.messages = []

        summary_exists = os.path.isfile('./summary.md')
        if summary_exists:
            with open('./summary.md', 'r') as file:
                self.project_summary = file.read()
        else:
            self.project_summary = ''
    
    def print_token_count(self,response):

        """
        Prints the token count used for the current call and updates the total token count.

        Args:
            response (Response): The response object containing usage information,
                                 including the number of tokens used in the call.
        """
        token_count = response.usage.total_tokens
        self.total_tokens += token_count
        agent = self.__class__.__name__
        print(f"Tokens use by {agent} Agent for this call: {token_count}\nTotal tokens used by {agent} Agent: {self.total_tokens}")
        




        
