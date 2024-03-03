import json
from openai import OpenAI

import fumedev.env as env

def jsonify_text(text):
    client = OpenAI()
    jsonify_messages = [{'role': 'system', 'content': 'Your job is turning the given JSON obejct in text into a valid JSON object. Do not change the content of the JSON object. Only format it as a valid JSON. There may be non-json texts around it, ignore them.'}, {'role': 'user', 'content': f'Here is thye text you have to turn into the JSON format:\n{text}\n\nYou response must be a valid JSON'}]
    response = client.chat.completions.create(
        model='gpt-4-0125-preview',
        messages=jsonify_messages,
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)