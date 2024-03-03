import json

from openai import OpenAI
from fumedev import env

from fumedev.prompts import split_complex_task_system, split_complex_task_user, turn_task_into_json_system, turn_task_into_json_user

def split_complex_task(task):
        messages = [
            {'role': 'system', 'content': split_complex_task_system()},
            {'role': 'user', 'content': split_complex_task_user(task=task)}
        ]

        client = OpenAI(api_key=env.OPENAI_API_KEY, base_url=env.BASE_URL)
        response = client.chat.completions.create(
            model=env.BASE_MODEL,
            messages=messages,
        )
        return turn_task_into_json(response.choices[0].message.content)


def turn_task_into_json(task):
        messages = [
            {'role': 'system', 'content': turn_task_into_json_system()},
            {'role': 'user', 'content': turn_task_into_json_user(task=task)}
        ]

        client = OpenAI(api_key=env.OPENAI_API_KEY, base_url=env.BASE_URL)
        response = client.chat.completions.create(
            model=env.BASE_MODEL,
            messages=messages,
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)