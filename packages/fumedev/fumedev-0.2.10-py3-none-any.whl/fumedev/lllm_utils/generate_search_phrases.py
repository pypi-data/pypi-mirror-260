from .jsonify_text import jsonify_text

import json

from openai import OpenAI

from fumedev import env

from fumedev.prompts import generate_search_phrases_system, generate_search_phrases_user, generate_search_phrases_system_slack
from fumedev.utils.get_dir_structure import get_dir_structure_bfs
from fumedev.utils.get_unique_extensions import get_unique_extensions

def generate_search_phrases(task, medium='cli'):
        
        extensions = get_unique_extensions(env.absolute_path('./codebase'))

        extension_str = ''
        for ext in extensions:
            extension_str += f"- {ext}\n"
        
        if medium == "slack":
            system_prompt = generate_search_phrases_system_slack(get_dir_structure_bfs())
        else:
            system_prompt = generate_search_phrases_system(task, get_dir_structure_bfs())

        if medium == 'cli':

            messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': generate_search_phrases_user()}
            ]
            
            client = OpenAI(api_key=env.OPENAI_API_KEY,base_url=env.BASE_URL)
            response = client.chat.completions.create(
                model=env.BASE_MODEL,
                messages=messages,
                response_format={"type": "json_object"},
            )
            search_phrases = json.loads(response.choices[0].message.content)['search']
        else:

            client = OpenAI()
            response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {'role': 'system', 'content': system_prompt},
                {
                "role": "user",
                "content": task
                }
            ],
            max_tokens=4096,
            )
            response_content = response.choices[0].message.content
            json_res = jsonify_text(response_content)
            search_phrases = json_res.get('search', [])

        return search_phrases
