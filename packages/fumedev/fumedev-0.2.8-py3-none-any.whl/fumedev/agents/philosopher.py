import asyncio
import json
from openai import OpenAI
from fumedev.prompts import philosopher_apply_feedback_prompt_1, philosopher_apply_feedback_system_prompt, philosopher_generate_step_system_prompt, philosopher_generate_step_user_prompt_1, philosopher_generate_step_user_prompt_2, philosopher_generate_step_user_prompt_3, philosopher_generate_step_user_prompt_create_file
from fumedev import env
from fumedev.agents.agent import Agent
from fumedev.utils.create_file import create_file
from fumedev.utils.find_closest_file_path import find_closest_file_path

class Philosopher (Agent):
    """
    Represents a specialized Agent capable of handling philosophical inquiries or tasks.
    This class extends the Agent class, leveraging OpenAI models to process tasks with a systematic approach,
    potentially involving multiple steps, feedback application, and specific contextual handling.
    It maintains state related to the task, such as messages, diffs, and snippets, to generate appropriate responses.
    """
    def __init__ (self, task, snippets=[], diffs=[], short_snippets=[]):
        """
        Initializes a new instance of the Philosopher class.

        Parameters:
        - task (str): The task description or query to be processed.
        - snippets (list): A list of code snippets (strings) relevant to the task.
        - diffs (list): A list of diffs (strings) representing changes made during task processing.
        - short_snippets (list): A concise version of snippets for summary or display purposes.
        """
        super().__init__()
        self.messages = []
        self.task = task
        self.snippets = snippets
        self.diffs = diffs
        self.short_snippets = short_snippets
        self.client = OpenAI(api_key=env.OPENAI_API_KEY, base_url=env.BASE_URL)
        self.tools = []
        

    def generate_step(self, future_thought="", feedback="", old_file="", old_plan=""):
        """
        Generates and processes the next step in handling the task based on current state and optionally a future thought.

        Parameters:
        - future_thought (str): An optional string hint or direction for generating the next step.

        Returns:
        A tuple containing the response content, future direction or thought, selected file paths,
        and the selected snippets based on the tool's interactions.
        """
        diff_str = '\n\n'.join(self.diffs)
        self.messages = [{"role": "system", "content": philosopher_generate_step_system_prompt(diff_str=diff_str, file_paths_str=self._format_files_str(snippets=self.short_snippets), feedback=feedback, old_file=old_file, old_plan=old_plan)},
                         {"role": "user", "content": philosopher_generate_step_user_prompt_1(task=self.task, future_thought=future_thought, feedback=feedback)}]
        
        self.tools = [
                        {
                            "name": "select_file",
                            "description": "Call this function when you want to select a file to make changes on it. As a result, you will be given the relevant snippets inside this file.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "file_path": {
                                        "type": "string",
                                        "description": "The exact file path you want to select",
                                    },
                                },
                                "required": ["file_path"],
                            },
                        },
                        {
                            "name": "done",
                            "description": "Call this function when you are sure you have covered all of necessary steps and completed the entirety of the task. He does not know anything about your current progress. He does not have memory of your previous questions or your actions.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "confidence": {
                                        "type": "string",
                                        "description": "How confident are you with your respone out of 10?",
                                    },
                                },
                                "required": ["confidence"],
                            },
                        },
                        {
                            "name": "create_file",
                            "description": "Call this function when you want to create a new file in the codebase. You will need to specify the file path where the new file should be created.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "file_path": {
                                        "type": "string",
                                        "description": "The file path where the new file will be created, including the name of the new file.",
                                    },
                                },
                                "required": ["file_path"],
                            },
                        },
                ]
        
        response = self.client.chat.completions.create(
            model=env.BASE_MODEL,
            messages=self.messages,
            functions=self.tools
        )

        response_message = response.choices[0].message
        self.messages.append(response_message)
        tool_call = response_message.function_call

        while True:
            didSelectFile = False
            didCreateFile = False
            file_paths = []
            selected_snippets = []
            if tool_call:
                
                    function_name = tool_call.name
                    args = json.loads(tool_call.arguments)

                    if function_name == 'select_file':
                        file_path = find_closest_file_path(env.absolute_path(args['file_path']))
                        file_paths.append(file_path)
                        print(f"\nLooking at {file_path}")
                        snip_str = self._format_snippets_str(self.snippets, file_path=file_path)
                        self.messages.append({'role': 'function', 'name': function_name,'content': snip_str})
                        selected_snippets.append({'file_path': file_path, 'code': snip_str})
                        didSelectFile = True
                      
                    elif function_name == 'done':
                        print('I decided that the task is complete.')
                        return False
                    elif function_name == 'create_file':
                        file_path = env.absolute_path(args['file_path'])
                        create_file(file_path)
                        self.messages.append({'role': 'function',  'name': function_name, 'content': f"File created at {env.relative_path(file_path)}"})
                        file_paths.append(file_path)
                        didCreateFile = True
                
            if didSelectFile:
                    self.messages.append({'role': 'user', 'content': philosopher_generate_step_user_prompt_2()})
                    stream = self.client.chat.completions.create(
                        model=env.BASE_MODEL,
                        messages=self.messages,
                        stream=True,
                    )
                    collected_messages = []
                    for chunk in stream:
                        if chunk.choices[0].delta.content is not None:
                            chunk_message = chunk.choices[0].delta.content  # extract the message
                            collected_messages.append(chunk_message) 
                            print(chunk_message, end="")

                    collected_messages = [m for m in collected_messages if m is not None]
                    full_reply_content = ''.join([m for m in collected_messages])

                    self.messages.append({'role': 'assistant', 'content': full_reply_content})

                    return full_reply_content, file_paths , selected_snippets, False
                
            elif didCreateFile:
                    self.messages.append({'role': 'user', 'content': philosopher_generate_step_user_prompt_create_file()})
                    stream = self.client.chat.completions.create(
                        model=env.BASE_MODEL,
                        messages=self.messages,
                        stream=True,
                    )
                    
                    collected_messages = []
                    for chunk in stream:
                        if chunk.choices[0].delta.content is not None:
                            chunk_message = chunk.choices[0].delta.content  # extract the message
                            collected_messages.append(chunk_message) 
                            print(chunk_message, end="")

                    collected_messages = [m for m in collected_messages if m is not None]
                    full_reply_content = ''.join([m for m in collected_messages])

                    return full_reply_content, file_paths , selected_snippets , True
            else:
                response_message = response.choices[0].message
                self.messages.append(response_message)
                tool_call = response_message.tool_calls


    def apply_feedback(self , action, feedback ,file_path, current_snippets):
        """
        Applies user feedback to the current task step, updating the task processing path accordingly.

        Parameters:
        - action (str): The specific action to which the feedback is applied.
        - feedback (str): The user-provided feedback to refine the task processing.
        - file_path (str): The path of the file related to the current task step and feedback.
        - current_snippets (list): A list of the current code snippets involved in feedback application.

        Returns:
        The full reply content after feedback is applied and integrated into task processing.
        """
        return self.generate_step(feedback=feedback, old_file=file_path, old_plan=action)
    
    def _format_snippets_str(self, snippets, file_path=None):
        res = ""
        if file_path:
            for s in snippets:
                if s.get('file_path') == file_path:
                    if not res:
                        res = f"# {env.relative_path(file_path)}\n{s.get('code')}"
                    else:
                        pass
            
            return res
        else:
            return "Error: No File Path Provided"
        
    def _format_all_snippets_str(self, snippets):
        res = ""
        for s in snippets:
            res += f"## {env.relative_path(s.get('file_path'))}\n{s.get('code')}\n\n"
        return res
        
    def _format_files_str(self, snippets):
        res = ""

        for snippet in snippets:
            res += f'''
            
## File Path {env.relative_path(snippet.get('file_path'))}
{snippet.get('code')}

'''

        return res


    
        