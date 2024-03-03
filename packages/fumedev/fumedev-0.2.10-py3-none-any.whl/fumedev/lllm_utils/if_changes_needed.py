import json

from openai import OpenAI
from fumedev import env

from fumedev.prompts import if_changes_needed_system, if_changes_needed_user

def if_changes_needed(speech):
        messages = [
            {'role': 'system', 'content': if_changes_needed_system()},
            {'role': 'user', 'content': if_changes_needed_user(speech=speech)}
        ]

        client = OpenAI(api_key=env.OPENAI_API_KEY,base_url=env.BASE_URL)
        response = client.chat.completions.create(
            model=env.BASE_MODEL,
            messages=messages,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)