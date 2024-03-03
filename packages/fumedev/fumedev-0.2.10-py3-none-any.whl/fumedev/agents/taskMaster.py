import json
import uuid
import tiktoken
from openai import OpenAI
import fumedev.env as env
from fumedev.agents.agent import Agent
from fumedev.prompts import task_master_system_prompt, task_master_user_prompt
from fumedev.utils.process_snippets import process_snippets
from fumedev.utils.search_snippet import search_snippet

class TaskMaster(Agent):
    def __init__(self, task, snippets, medium="cli"):
        self.messages = []
        self.task = task
        self.snippets = snippets
        self.medium = medium
        self.client = OpenAI(base_url=env.BASE_URL, api_key=env.OPENAI_API_KEY)

    def solve(self, feedback="", old_plan="", iteration=0):

        if feedback:
            env.posthog.capture(env.USER_ID, event='task_feedback', properties={'task': env.TASK, 'task_id': env.TASK_ID})
        else:
            env.TASK_ID = str(uuid.uuid4())
            env.posthog.capture(env.USER_ID, event='task_start', properties={'task': env.TASK, 'task_id': env.TASK_ID})


        context = self._generate_context()
        if not context:
            print('Too many files in the context')
            return False
        
        self.messages = [{'role': 'system', 'content': task_master_system_prompt(context=context)},
                         {'role': 'user', 'content': task_master_user_prompt(task=self.task, feedback=feedback, old_plan=old_plan, medium=self.medium)}]
        
        response = self.client.chat.completions.create(model=env.BASE_MODEL, messages=self.messages, max_tokens=4096)
        response_message = response.choices[0].message

        plan = response_message.content

        plan_json = self.organize(solution=plan)  

        steps = plan_json.get('steps', [])

        for step in steps:
            if not step.get('sufficient'):
                if iteration < 5:
                    task = f"# {step.get('title', '')}\n {step.get('text', '')}"
                    snip_lst, _ = search_snippet(query=step.get('title', ''), k=5)
                    meta_task_master = TaskMaster(task=task, snippets=self.snippets + snip_lst)
                    detailed_plan = meta_task_master.solve(iteration=iteration+1)
                    plan += f"\nDetailed Explanation About {step.get('title', '')}\n{detailed_plan}"
                    
        return plan

    def _generate_context(self, max_tokens = 70000):
        encoding = tiktoken.encoding_for_model(env.BASE_MODEL)
        increment = 100
        iteration = 1
        num_tokens = 0

        while num_tokens < max_tokens:
            context_files = process_snippets(snippets=self.snippets, lines_before=increment*iteration, lines_after=increment*iteration)
            context_str = self._format_snippets(snippets=context_files)
            new_num_tokens = len(encoding.encode(context_str))
            iteration += 1
            if new_num_tokens == num_tokens:
                break
            else:
                num_tokens = new_num_tokens

        if iteration == 1:
            return False
        else:
            context_files = process_snippets(snippets=self.snippets, lines_before=increment*(iteration-1), lines_after=increment*(iteration-1))
            context_str = self._format_snippets(snippets=context_files)
            return context_str
        
    def organize(self, solution):
        system_message = "You are an extremely smart and organized AI software engineer. You will be given plan to implement a coding task in multiple files. Your job is turn the steps descirbed in this plan into a list of JSON objects in the following format:"
        system_message +="""

{"steps": [
    {
        "title": "{THE TITLE FOR THE STEP}",
        "content": "{The deatiled description of the step including all of the code and the reasoning}"
        "sufficient": {True or False depending on the level of detail the step is explained. For a step to be sufficient, it should CLEARY explain an ACTIONABLE change in a SINGLE code file}
    },
    {
        "title": "{THE TITLE FOR THE STEP}",
        "content": "{The deatiled description of the step including all of the code and the reasoning}"
        "sufficient": {True or False depending on the level of detail the step is explained. For a step to be sufficient, it should CLEARY explain an ACTIONABLE change in a SINGLE code file}
    },
    {
        "title": "{THE TITLE FOR THE STEP}",
        "content": "{The deatiled description of the step including all of the code and the reasoning}"
        "sufficient": {True or False depending on the level of detail the step is explained. For a step to be sufficient, it should CLEARY explain an ACTIONABLE change in a SINGLE code file}
    }
    ...
]}

"""

        system_message += "Here are the set of rules you must obey:\n* You must cover all of the plan without leaving any described detail.\n* You must be very specific with your plan. You can include code in your content if it's in the original solution\n* Strictly obey to the JSON format.\n* The string in the contenb field can be as long as you need. More the detail the better.\n* 'sufficient' field is very important. You must decide if the step described is an actionable change in a SINGLE code file. A step is NOT sufficient, if it describes a change in multiple files, if it describes searching something in the codebase or has incomplete logic to implement the code.\n* Merge all of the steps for single file under a single step.\n* Every sufficient step is a description of all of the changes needed in a single file. You can merge should if they are for the same file."

        user_message = f"Here is the solution you have to turn into an organized plan:\n{solution}"

        messages = [{'role': 'system', 'content': system_message}, {'role': 'user', 'content': user_message}]
        response = self.client.chat.completions.create(model='gpt-4-0125-preview', messages=messages, response_format={"type": "json_object"},)

        response_message_content = response.choices[0].message.content

        return json.loads(response_message_content)


    def _format_snippets(self, snippets):
        res = ""

        for s in snippets:
            res += f"# File Path: {env.relative_path(s.get('file_path'))}\n{s.get('code')}\n\n"

        return res
