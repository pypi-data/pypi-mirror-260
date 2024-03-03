import copy
import os
from dotenv import load_dotenv
from fumedev.agents.coderMinion import CoderMinion

from fumedev.agents.philosopher import Philosopher
from fumedev.git_ops.createPR import submit_code
from fumedev.git_ops.utils import move_to_branch, pull_repo
from fumedev.index.Documentation import Documentation
from fumedev.lllm_utils.if_changes_needed import if_changes_needed
from fumedev.lllm_utils.split_complex_task import split_complex_task
from fumedev.utils.create_diff import create_diff
from fumedev.utils.fetch_and_encode_image import fetch_and_encode_image
from fumedev.utils.process_snippets import process_snippets
load_dotenv()
from slack_bolt import App, BoltResponse
from slack_bolt.oauth.callback_options import CallbackOptions, SuccessArgs, FailureArgs
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_sdk import WebClient

from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

# Load environment variables (make sure SLACK_BOT_TOKEN and SLACK_SIGNING_SECRET are set)
import fumedev.env as env 
from fumedev.lllm_utils.generate_search_phrases import generate_search_phrases
from fumedev.utils.search_snippet import search_snippet
from fumedev.agents.taskMaster import TaskMaster
from fumedev.utils.remove_at_words import remove_at_words

env.CLOUD_HOSTED = True
env.OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Callback to run on successful installation
def success(args: SuccessArgs) -> BoltResponse:
    # Call default handler to return an HTTP response
    return args.default.success(args)
    # return BoltResponse(status=200, body="Installation successful!")


# Callback to run on failed installation
def failure(args: FailureArgs) -> BoltResponse:
    return args.default.failure(args)
    # return BoltResponse(status=args.suggested_status_code, body=args.reason)

# Initialization
app = App(
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    installation_store=FileInstallationStore(),
    oauth_settings=OAuthSettings(
        client_id=os.environ.get("SLACK_CLIENT_ID"),
        client_secret=os.environ.get("SLACK_CLIENT_SECRET"),
        scopes=["app_mentions:read", "channels:history", "chat:write", "commands", "reactions:read", "reactions:write"],
        user_scopes=[],
        redirect_uri=f"{env.SLACK_REDIRECT_HOST}/slack/oauth_redirect",
        install_path="/slack/install",
        #redirect_uri_path="/slack/oauth_redirect",
        state_store=FileOAuthStateStore(expiration_seconds=600),
        callback_options=CallbackOptions(success=success, failure=failure),
    ),
)

def get_token_for_team(team_id):
    # Assuming you have a function or method to retrieve the installation data
    # for a given team_id from your installation store
    try:
        installation = app.installation_store.find_installation(team_id=team_id, enterprise_id=None)
        # Your code here
    except Exception as e:
        # Log the error or send it to a debugging channel
        print(f"Error finding installation: {e}")

    if installation:
        return installation.bot_token  # Or `access_token` depending on your app's scopes and installation details
    else:
        raise Exception(f"No installation found for team: {team_id}")

# Function to process a single message (for text and images) 
def process_message(message):
    text = message.get('text', '')
    print(f"Message Text: {text}") 

    if 'files' in message:
        for file in message['files']:
            if file.get('filetype') == 'image':  
                image_url = file['url_private']  # Or appropriate URL variant
                print(f"Image Found: {image_url}")
                # Do something with the image URL

@app.message()
def handle_message_events(message, say):
    # Check if the message is part of a specific thread
    specific_thread_ts = globals().get("THREAD_TS", '')
    if message.get('thread_ts') == specific_thread_ts:
        # Respond to the message or perform your logic here
        stage = globals()["STAGE"]
        text = message['text']

        if stage == "FILE_SELECTION":
            add_file_util(text=text, say=say)
        elif stage == "PLAN":
            plan_feedback_util(feedback=text, say=say)
        else:
            return

@app.event("app_mention")
def handle_mention(event, say, client):

    channel_id = event['channel'] 
    thread_ts = event.get('thread_ts', event['ts'])
    globals()["THREAD_TS"] = thread_ts

    if not env.IS_WORKING:
        env.IS_WORKING = True
        globals()["STAGE"] = "INITIAL"
    else:
        say("Sorry, I'm working on another task right now. Can you try this later?:slightly_frowning_face:\nFume team is currently working on enabling multi-tasking...", thread_ts=thread_ts)
        return

    team_id = event["team"]
    
    try:
        # Retrieve the access token for the team
        token = get_token_for_team(team_id)
    except Exception as e:
        say(text=f"Failed to retrieve token: {e}", thread_ts=thread_ts)
        return

    # React to the mention with eyes emoji
    client.reactions_add(
        channel=event['channel'],
        timestamp=event['ts'],
        name="eyes"
    )

    pull_repo()
    move_to_branch(env.base_branch)
    env.append_hidden_folders_to_exclude()
    env.parse_gitignore()
    dc = Documentation()
    dc.document()


    globals()["TEMP_FILE_PATHS"] = []

    formatted_messages = []  # Initialize an empty list to store message information

    try:
        result = client.conversations_replies(
            channel=channel_id,
            ts=thread_ts
        )
        messages = result['messages']
        for message in messages:
            # Handle text content of the message
            if message.get('text', ''):
                formatted_messages.append({"type": "text", "text": message['text']})

            # Handle files (including images) attached to the message
            if 'files' in message:
                for file in message['files']:
                    if file['mimetype'].startswith('image/'):
                        image_url = file['url_private']
                        try:
                            # Fetch and encode the image using the retrieved token
                            encoded_image, mime_type = fetch_and_encode_image(image_url, token)
                            # Use the MIME type dynamically to construct the data URL
                            formatted_messages.append({"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{encoded_image}"}})
                        except Exception as e:
                            print(f"Error fetching and encoding image: {e}")

            # Handle images embedded in blocks (optional)
            if 'blocks' in message:
                for block in message['blocks']:
                    if block['type'] == 'image':
                        image_url = block['image_url']
                        try:
                            # Fetch and encode the image using the retrieved token
                            encoded_image, mime_type = fetch_and_encode_image(image_url, token)
                            # Use the MIME type dynamically to construct the data URL
                            formatted_messages.append({"type": "image_url", "image_url": {"url": f"data:{mime_type},{encoded_image}"}})
                        except Exception as e:
                            print(f"Error fetching and encoding image: {e}")

        env.BASE_MODEL = "gpt-4-vision-preview"

        task = []

        for message in formatted_messages:
            if message.get('type') == "text":
                message["text"] = remove_at_words(text=message.get("text"))
                task.append(message)
            else:
                task.append(message)

        env.TASK = formatted_messages
        phrases = generate_search_phrases(task=formatted_messages, medium="slack")

        file_paths = []

        for phrase in phrases:

            query = phrase.get('phrase')
            extension = phrase.get('file_extension')

            snip_lst, files = search_snippet(query=query, extension=extension)

            file_paths += files
            file_paths = list(set(file_paths))

            env.SNIPPETS += snip_lst 

        options = []
        globals()["TEMP_FILE_PATHS"] = file_paths

        for idx, p in enumerate(file_paths):
            option = {
                        "text": {
                            "type": "mrkdwn",
                            "text": env.relative_path(path= p)
                        },
                        "value": p
                    }
            options.append(option)

        globals()["OPTIONS"] = options

        blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Here are the files I selected for this task. Please unselect the ones you think are irrelevant or add more telling me what you wanna search for in the codebase."
                    },
                    "accessory": {
                        "type": "checkboxes",
                        "options": options[:10],
                        "initial_options": options[:10],
                        "action_id": "checkboxes_action"
                    }
                },
                {
                "type": "actions",
                "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Done"
                            },
                            "action_id": "done_button"
                        }
                    ]
                }
        ]

        # Now formatted_messages contains all messages in the specified format
        say(
            blocks=blocks,
            text=f"Hi, I selected relevant files for the task!",
            thread_ts=thread_ts
        )
        
        globals()["STAGE"] = "FILE_SELECTION"

    except Exception as e:
        print(f"Error fetching thread messages: {e}")

# Helper function: Assumes threads are simple sequences before the mention
def find_original_message(messages, mention_ts):
    for message in messages:  # Iterate in reverse for efficiency 
        if message['ts'] > mention_ts:  # If the message is older than the mention
            continue
        else:
            return

@app.action("done_button")
def handle_done_button(ack, body, client, say):
    # Acknowledge the button click
    ack()

    channel_id = body['channel']['id']
    message_ts = body['message']['ts']
    
    # Assume we have the original blocks and we know the button block's structure or position
    original_blocks = body['message']['blocks']
    
    # Create a new blocks list excluding the button blocks
    new_blocks = [block for block in original_blocks if not (block['type'] == 'actions')]
    
    # Optionally, add a new block with a message acknowledging the action taken
    new_blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":hourglass_flowing_sand: Planning what to do..."
        }
    })

    # Update the original message to remove the button blocks
    client.chat_update(
        channel=channel_id,
        ts=message_ts,
        blocks=new_blocks,
        text=":hourglass_flowing_sand: Planning what to do..."  # This is the fallback text for notifications and should be adjusted as needed.
    )

    if not globals().get('FILE_PATHS'):
        globals()["FILE_PATHS"] = []

    if not globals().get('TEMP_FILE_PATHS'):
        globals()["TEMP_FILE_PATHS"] = []
    else:
        globals()["FILE_PATHS"] += globals().get('TEMP_FILE_PATHS')
        globals()["TEMP_FILE_PATHS"] = []

    if not globals().get('FILE_PATHS'):
        say(":x: At least 1 file must be in the context!", thread_ts=globals().get("THREAD_TS"))
        return

    file_paths = globals()["FILE_PATHS"]

    new_snippets = []

    for snip in env.SNIPPETS:
        in_files = False

        for file in file_paths:
            if file in snip.get('file_path'):
                in_files = True
                break

        if in_files:
            new_snippets.append(snip)

    env.SNIPPETS = new_snippets

    task_master = TaskMaster(task=env.TASK, snippets=env.SNIPPETS, medium="slack")
    plan = task_master.solve()
    globals()['PLAN'] = plan

    globals()["STAGE"] = "PLAN"

    plan_paragraphs = plan.split('\n\n')

    blocks = []
    for paragraph in plan_paragraphs:
        while len(paragraph) > 3000:
            part = paragraph[:3000]
            end_index = part.rfind("\n")
            if end_index == -1:
                end_index = 3000

            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": paragraph[:end_index]}})
            paragraph = paragraph[end_index:]

        if paragraph:
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": paragraph}})
    start_block = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Here is the plan I came up with:\n\nDoes this plan look good to you?"
        },
    }

    confirmation_blocks = [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Yes"
                    },
                    "action_id": "plan_yes_button"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "No"
                    },
                    "action_id": "plan_no_button"
                }
            ]
        }
    ]

    blocks = [start_block] + blocks + confirmation_blocks

    say(blocks=blocks, text="I'm done with the plan! Can you please review it?", thread_ts=globals().get("THREAD_TS"))

@app.action("plan_no_button")
def handle_plan_rejection(ack, body, client, say):
    ack()
    # Extract the channel ID and message timestamp from the action's body
    channel_id = body['channel']['id']
    message_ts = body['message']['ts']

    globals()['FEEDBACK_MODE'] = "task_master"
    
    # Assume we have the original blocks and we know the button block's structure or position
    original_blocks = body['message']['blocks']
    
    # Create a new blocks list excluding the button blocks
    new_blocks = [block for block in original_blocks if not (block['type'] == 'actions')]
    
    # Optionally, add a new block with a message acknowledging the action taken
    new_blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "The plan has been rejected. How should I change it? Please use /edit tool to give feedback."
        }
    })

    # Update the original message to remove the button blocks
    client.chat_update(
        channel=channel_id,
        ts=message_ts,
        blocks=new_blocks,
        text="Updated message after plan rejection."  # This is the fallback text for notifications and should be adjusted as needed.
    )

@app.action("plan_yes_button")
def handle_plan_approval(ack, body, say, client):
    ack()

    globals()["STAGE"] = "CODE"

    env.BASE_MODEL = 'gpt-4-0125-preview'

    channel_id = body['channel']['id']
    message_ts = body['message']['ts']
    
    # Assume we have the original blocks and we know the button block's structure or position
    original_blocks = body['message']['blocks']
    
    # Create a new blocks list excluding the button blocks
    new_blocks = [block for block in original_blocks if not (block['type'] == 'actions')]
    
    # Optionally, add a new block with a message acknowledging the action taken
    new_blocks.append({
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": ":technologist: Writing the code..."
        }
    })

    # Update the original message to remove the button blocks
    client.chat_update(
        channel=channel_id,
        ts=message_ts,
        blocks=new_blocks,
        text=":technologist: Writing the code..."
    )

    diffs = []
    isDone = False

    while not isDone:
        snippets_copy = copy.deepcopy(env.SNIPPETS)
        processed_snippets = process_snippets(snippets=snippets_copy)

        phil = Philosopher(task=globals()["PLAN"], snippets=processed_snippets, short_snippets=env.SNIPPETS, diffs=diffs)

        res = phil.generate_step()

        if res:
            action, file_paths, current_snippets, new_file = res

            if len(file_paths) > 1:
                print_files = ', '.join([env.relative_path(f) for f in file_paths])
            else:
                print_files = env.relative_path(file_paths[0])

            action_word = "modified"

            if new_file:
                diffs.append(f"* You created {print_files}. Here is what you did:\n{action}")

                CoderMinion(task=action, file_paths=file_paths).create_file()

                continue

            changes = if_changes_needed(speech=action)

            decision = changes.get('decision')
            is_multiple = changes.get('is_multiple')

            if decision:
                new_snippets = [snippet for snippet in env.SNIPPETS if not snippet.get('file_path') in file_paths]
                env.SNIPPETS = new_snippets

                diffs.append(f"* You {action_word} {print_files}. Here is what you did:\n{action}")
                if is_multiple:
                    old_files = []
                    for path in file_paths:
                        with open(path, 'r') as file:
                            old_files.append(file.read())

                    sub_tasks_dict = split_complex_task(action)

                    sub_tasks = sub_tasks_dict.get('plan')
                    for t in sub_tasks:

                        task = '# ' + t.get('task') + '\n' + '* ' + '\n'.join(t.get('steps'))

                        coder = CoderMinion(task=task, file_paths=file_paths)
                        coder.code()

                else:

                    old_files = []
                    for path in file_paths:
                        with open(path, 'r') as file:
                            old_files.append(file.read())

                    # Assuming 'action' is defined elsewhere and appropriate for 'task'
                    coder = CoderMinion(task=action, file_paths=file_paths)
                    coder.code()
            else:
                for path in file_paths:
                    diffs.append(f"* You decied no changes are necessary for {env.relative_path(path=path)}. There is no need to select them again. Here is your reasoning:\n {action}")

        else:
            isDone = True

    env.posthog.capture(env.USER_ID, event='task_done', properties={'task': env.TASK, 'task_id': env.TASK_ID})
    submit_code(plan=globals()["PLAN"])
    env.IS_WORKING = False
    say(":white_check_mark: Completed the task! Just submitted a PR!", thread_ts=globals().get("THREAD_TS"))

@app.action("checkboxes_action")
def handle_some_action(ack, body, logger):
    ack()  # Acknowledge the action
    logger.info(body)  # Log the body for debugging
    
    # The action ID of your checkbox, which you know
    action_id = "checkboxes_action"
    selected_files = []
    
    # Iterating through the state values to find our action_id
    for block_id, block in body['state']['values'].items():
        if action_id in block:
            selected_options = block[action_id]['selected_options']
            selected_files += [option.get('value') for option in selected_options] # Assuming only one set of checkboxes with this action_id

        else:
            # Log or handle the case where the action_id was not found in any block
            logger.info("Action ID not found in any blocks.")

    globals()["TEMP_FILE_PATHS"] = selected_files

def start_app():
    app.start(port=int(os.environ.get("PORT", 3000)))

def add_file_util(text, say):

    if not globals().get('FILE_PATHS'):
        globals()["FILE_PATHS"] = []

    if not globals().get('TEMP_FILE_PATHS'):
        globals()["TEMP_FILE_PATHS"] = []
    else:
        globals()["FILE_PATHS"] += globals().get('TEMP_FILE_PATHS')
        globals()["TEMP_FILE_PATHS"] = []

    say(f':mag: Searching "{text}"', thread_ts=globals().get("THREAD_TS"))

    phrases = text.split(',')

    file_paths = []

    for phrase in phrases:

        query = phrase.strip()

        snip_lst, files = search_snippet(query=query)

        snip_lst = [snip for snip in snip_lst if snip.get('file_path') not in globals()["FILE_PATHS"]]
        files = [f for f in files if f not in globals()["FILE_PATHS"]]

        file_paths += files
        file_paths = list(set(file_paths))

        env.SNIPPETS += snip_lst 

    options = []
    globals()["TEMP_FILE_PATHS"] += file_paths

    for idx, p in enumerate(file_paths):
        option = {
                    "text": {
                        "type": "mrkdwn",
                        "text": env.relative_path(path= p)
                    },
                    "value": p
                }
        options.append(option)

    globals()["OPTIONS"] = options

    if file_paths:
        blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Here a are the files I added to the context"
                    },
                    "accessory": {
                        "type": "checkboxes",
                        "options": options[:10],
                        "initial_options": options[:10],
                        "action_id": "checkboxes_action"
                    }
                },
                {
                "type": "actions",
                "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Done"
                            },
                            "action_id": "done_button"
                        }
                    ]
                }
            ]
    else:
        blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Couldn't find any files that are not already in the context :confused:"
                    },
                },
                {
                "type": "actions",
                "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Done"
                            },
                            "action_id": "done_button"
                        }
                    ]
                }
            ]

    # Now formatted_messages contains all messages in the specified format
    say(
        blocks=blocks,
        text=f"Hi, I selected relevant files for your query!",
        thread_ts=globals().get("THREAD_TS")
    )

def plan_feedback_util(feedback, say):
    say(f":writing_hand: Revising my plan with you feedback.", thread_ts=globals().get("THREAD_TS"))

    mode =  globals().get('FEEDBACK_MODE')

    if mode == 'task_master':
        task_master = TaskMaster(task=env.TASK, snippets=env.SNIPPETS, medium="slack")
        plan = task_master.solve(feedback=feedback, old_plan=globals()['PLAN'])
        globals()['PLAN'] = plan
    else:
        say("There is nothing to give feedback for? I think you made a mistake:confused:", thread_ts=globals().get("THREAD_TS"))
        return
    
    globals()['FEEDBACK_MODE'] = ""

    plan_paragraphs = plan.split('\n\n')

    blocks = []
    for paragraph in plan_paragraphs:
        while len(paragraph) > 3000:
            part = paragraph[:3000]
            end_index = part.rfind("\n")
            if end_index == -1:
                end_index = 3000

            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": paragraph[:end_index]}})
            paragraph = paragraph[end_index:]

        if paragraph:
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": paragraph}})
    start_block = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Here is the new plan I came up with:\n\nDoes this look good now?"
        },
    }

    confirmation_blocks = [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Yes"
                    },
                    "action_id": "plan_yes_button"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "No"
                    },
                    "action_id": "plan_no_button"
                }
            ]
        }
    ]

    blocks = [start_block] + blocks + confirmation_blocks

    say(blocks=blocks, text="I edited the plan! Can you please review it?", thread_ts=globals().get("THREAD_TS"))