import copy
import shutil
import time
import asyncio
import os
import sys
import threading
from typing import Coroutine
import sentry_sdk
from textual.app import ComposeResult
from textual.events import Click
from textual.screen import Screen
from textual.widgets import Label, Button, Static, Input, TextArea, Rule, LoadingIndicator
from textual.containers import Container, ScrollableContainer
from textual import work
from fumedev.agents.coderMinion import CoderMinion
from fumedev.agents.philosopher import Philosopher

import fumedev.env as env
from fumedev.index.Documentation import Documentation
from fumedev.lllm_utils.generate_search_phrases import generate_search_phrases
from fumedev.lllm_utils.if_changes_needed import if_changes_needed
from fumedev.lllm_utils.split_complex_task import split_complex_task
from fumedev.models.ChatLog import ChatLog
from fumedev.utils.copy_to_existing_directory import copy_to_existing_directory
from fumedev.utils.create_diff import create_diff
from fumedev.utils.create_git import create_git
from fumedev.utils.fliter_snippets_list import filter_snippets_list
from fumedev.utils.generate_id import generate_id
from fumedev.utils.process_snippets import process_snippets
from fumedev.utils.run_documentation import run_documentation
from fumedev.utils.search_snippet import search_snippet
from fumedev.agents.taskMaster import TaskMaster

class MultiChoice(Static):
    def __init__(self, options: list):
        super().__init__()
        self.options = options

    def on_mount(self):
        for idx, option in enumerate(self.options):
            self.query_one('#multiChoiceContainer').mount(Button(option, classes="multiChoiceOption", id=f"answer{idx}"))

    def compose(self) -> ComposeResult:
        yield Container(id="multiChoiceContainer")

class LoadingInput(Static):
    def compose(self) -> ComposeResult:
        yield Container(LoadingIndicator(), id="multiChoiceContainer")

class FileCardRemoveButton(Static):
    def __init__(self, removeAction):
        super().__init__()
        self.removeAction = removeAction

    def on_click(self):
        self.removeAction()

    def compose(self) -> ComposeResult:
        yield Container(Label('X'), id="fileCardRemove")

class FileCard(Static):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def remove_file_card(self):
        updated_snippets = [snippet for snippet in env.SNIPPETS if snippet.get('file_path') != self.file_path]
        env.SNIPPETS = updated_snippets

        self.remove()

    def compose(self) -> ComposeResult:
        display_path = self.file_path
        # Check if file_path is longer than 20 characters
        if len(self.file_path) > 35:
            display_path = "..." + self.file_path[-35:] # Select the last 20 characters and prepend with ellipsis
        yield Container(Label(display_path, id="fileCardLabel"), FileCardRemoveButton(removeAction=self.remove_file_card), id="fileCard")

class ContextFiles(Static):

    def __init__(self, context):
        super().__init__()
        self.context = context

    def on_mount(self):
        for file in self.context:
            new_file_card = FileCard(file)
            self.query_one("#selectedFilesScroll").mount(new_file_card)
            new_file_card.scroll_visible()

    def update_file_list(self, files):
        ## will be more complex in the future when the snippets come in
        self.context = files
        cards = self.query("FileCard")
        cards.remove()

        for file in self.context:
            new_file_card = FileCard(file)
            self.query_one("#selectedFilesScroll").mount(new_file_card)
            new_file_card.scroll_visible()

    def compose(self) -> ComposeResult:
        yield ScrollableContainer(Container(Button('Add Files', id='navigateFileSelector', disabled=True), Button('Search Phrase', id="navigateSearchPhrase", disabled=True), id="filesActionButtons"), id="selectedFilesScroll")


class ChatCard(Static):
    def __init__(self, role, content, id):
        super().__init__()
        self.role = role
        self.content = content
        self.id = id

    def compose(self) -> ComposeResult:
        yield Container(Label(self.role, id="chatCardRole"), TextArea(self.content, read_only=True, classes="chatCardContent", id=self.id), Rule(), id="chatCard")

class ChatDialogue(Static):
    def compose(self) -> ComposeResult:
        yield ScrollableContainer(id='chatScroll')

class ChatInput(Static):

    def __init__(self, value=""):
        super().__init__()
        self.value = value

    def compose(self) -> ComposeResult:
        yield Container(TextArea(language="markdown", id="userInput", text=self.value), Button('Submit', variant='success', id="submit"), id="chatInputContainer")

class ChatWindow(Static):
    def compose(self) -> ComposeResult:
        yield ScrollableContainer(ChatDialogue(id='chatDialogue'), ChatInput(), id="chatWindowContainer")

class Main(Screen):

    CSS_PATH = "./main.tcss"

    def __init__(self, context=[]):
        super().__init__()
        self.context = context
        self.answer_actions = []
        self.open_ended_action = None
        self.latest_user_input = ""
        env.SNIPPETS = []
        self.action = ""
        self.plan = ""
        sentry_sdk.init(
        dsn="https://e7d25c029a18008af886845658f130b0@o4506832139190272.ingest.sentry.io/4506832142532608",
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,     
    )
        self.diffs = []
        
    async def handle_exception(self, exception: Exception) -> None:
        print('Exception:', exception)
        sentry_sdk.capture_exception(exception)

    def enableContextEditButtons(self):
        buttons = self.query('#navigateFileSelector, #navigateSearchPhrase')
        for b in buttons:
            b.disabled = False

    def disableContextEditButtons(self):
        buttons = self.query('#navigateFileSelector, #navigateSearchPhrase')
        for b in buttons:
            b.disabled = True

    def ask_multi_choice(self, options):
        prompt = MultiChoice(options=options)
        self.query_one('ChatInput, MultiChoice, LoadingInput').remove()
        self.query_one('#chatWindowContainer').mount(prompt)

    def start_loading(self):
        prompt = LoadingInput()
        self.query_one('ChatInput, MultiChoice, LoadingInput').remove()
        self.query_one('#chatWindowContainer').mount(prompt)

    def ask_open_ended(self, action, value=""):
        prompt = ChatInput(value=value)
        self.open_ended_action = action
        self.query_one('ChatInput, MultiChoice, LoadingInput').remove()
        self.query_one('#chatWindowContainer').mount(prompt)

    def add_chat_log(self, log: ChatLog):
        new_card = ChatCard(role=log.role, content=log.content, id=log.id)
        scroll_container = self.query_one('#chatScroll')
        scroll_container.mount(new_card)
        scroll_container.scroll_end()

    def fume_print(self, content):
        log = ChatLog(role="Fume", content=content, id=generate_id())
        self.add_chat_log(log=log)

    def user_print(self, content):
        log = ChatLog(role="You", content=content, id=generate_id())
        self.add_chat_log(log=log)

    async def check_project(self):
        self.app.call_from_thread(self.start_loading)
        self.app.call_from_thread(self.fume_print, content="Welcome! Let's get started!")
        # Ask for the project path
        project_path = os.getcwd()
        env.PROJECT_PATH = project_path

        # Define the destination directory
        destination_dir = env.absolute_path('./codebase')

        if os.path.exists(destination_dir):
            shutil.rmtree(destination_dir)
        # Create the destination directory if it does not exist
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        else:
            for filename in os.listdir(destination_dir):
                file_path = os.path.join(destination_dir, filename)
                try:
                    # If it is a file, delete it
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    # If it is a directory, delete it and all its contents
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    env.CHAT_LOG.append(ChatLog(role="ERROR", content="Something went wrong. Please try another time.", id=generate_id()))
                    print(f'Failed to delete {file_path}. Reason: {e}')\

        # Copy the project directory to the new location
        # If the destination directory is empty, use copytree directly with exclusion
        self.app.call_from_thread(self.fume_print, content='Reading the workspace...')
        if not os.listdir(destination_dir):
            shutil.copytree(project_path, destination_dir, ignore=shutil.ignore_patterns('.git'), dirs_exist_ok=True)
            create_git(destination_dir)
        else:
            # If destination directory exists and is not empty, copy contents manually excluding .git
            copy_to_existing_directory(project_path, destination_dir)
            create_git(destination_dir)



        env.append_hidden_folders_to_exclude()
        env.parse_gitignore()
        self.app.call_from_thread(self.fume_print, content=f'Is this the directory you want to work on: {project_path}?')

        self.answer_actions = [self.ask_task, self.exit_with_message]
        self.app.call_from_thread(self.ask_multi_choice, options=['Yes', 'No'])

    async def ask_task(self):
        self.app.call_from_thread(self.fume_print, content=f'What are we working on today?')
        self.app.call_from_thread(self.ask_open_ended, action=self.solve_task)

    def update_context_files_display(self, files):
        context_files = self.query_one('ContextFiles')
        context_files.context += files
        context_files.context = list(set(context_files.context))
        cards = self.query("FileCard")
        cards.remove()

        for file in context_files.context:
            new_file_card = FileCard(file)
            self.query_one("#selectedFilesScroll").mount(new_file_card)
            new_file_card.scroll_visible()

    async def solve_task(self):
        task = self.latest_user_input
        self.app.call_from_thread(self.enableContextEditButtons)
        env.TASK = task
        self.app.call_from_thread(self.start_loading)
        self.app.call_from_thread(self.fume_print, content=f"Processing your codebase...(This may take 5-10 minutes the first time you are running Fume on a workspace)")
        run_documentation()

        self.app.call_from_thread(self.fume_print, content=f"Thinking of files to search...")

        phrases = generate_search_phrases(task=task)

        phrases_str = '\n- ' + '\n- '.join([obj.get('phrase') for obj in phrases])
        self.app.call_from_thread(self.fume_print, content=phrases_str)

        file_paths = []

        for phrase in phrases:

            query = phrase.get('phrase')
            extension = phrase.get('file_extension')

            self.app.call_from_thread(self.fume_print, content=f"Searching '{query}'")
            snip_lst, files = search_snippet(query=query, extension=extension)

            file_paths += files

            env.SNIPPETS += snip_lst 

        

        file_paths = list(set(file_paths))

        self.app.call_from_thread(self.update_context_files_display, files=file_paths)

        self.app.call_from_thread(self.fume_print, content=f"I selected the files that I think are relevant for this task. Please edit the context as necessary -->")

        self.isDoneEditing = False

        self.answer_actions = [self.make_plan]
        self.app.call_from_thread(self.ask_multi_choice, options=["Done"])

    async def make_plan(self):
        self.app.call_from_thread(self.start_loading)
        self.app.call_from_thread(self.fume_print, content="Creating a plan for the task")
        task_master = TaskMaster(task=env.TASK, snippets=env.SNIPPETS)
        plan = task_master.solve()
        self.plan = plan

        self.app.call_from_thread(self.fume_print, content=plan)
        self.app.call_from_thread(self.fume_print, content='Does this plan look good to you?')

        self.answer_actions = [self.start_philly, self.get_feedback_on_plan]
        self.app.call_from_thread(self.ask_multi_choice, options=['Yes', 'No'])

    async def get_feedback_on_plan(self):
        self.app.call_from_thread(self.fume_print, content="How should I change the plan?")
        self.app.call_from_thread(self.ask_open_ended, action=self.iterate_plan)

    async def iterate_plan(self):
        self.app.call_from_thread(self.start_loading)
        task_master = TaskMaster(task=env.TASK, snippets=env.SNIPPETS)
        plan = task_master.solve(feedback=self.latest_user_input, old_plan=self.plan)
        self.plan = plan

        self.app.call_from_thread(self.fume_print, content=plan)
        self.app.call_from_thread(self.fume_print, content='Is the plan good now?')

        self.answer_actions = [self.start_philly, self.get_feedback_on_plan]
        self.app.call_from_thread(self.ask_multi_choice, options=['Yes', 'No'])

    async def start_philly(self):
        if not env.SNIPPETS:

            self.notify('No files left in the context', severity='info')
            self.app.call_from_thread(self.fume_print, "I have looked at all of the relevant files.")
            env.posthog.capture(env.USER_ID, event='task_done', properties={'task': env.TASK, 'task_id': env.TASK_ID})
            self.app.call_from_thread(self.fume_print, "What's next?")
            self.app.call_from_thread(self.ask_open_ended, action=self.solve_task)
            return
        
        task = self.plan

        self.app.call_from_thread(self.start_loading)

        snippets_copy = copy.deepcopy(env.SNIPPETS)
        processed_snippets = process_snippets(snippets=snippets_copy)


        ## REFACTOR THE DIFFS TO BE MORE ACCURATE
        phil = Philosopher(task=task, snippets=processed_snippets, short_snippets=env.SNIPPETS, diffs=self.diffs)

        self.app.call_from_thread(self.fume_print, content='Thinking about what to do...')   
        res = phil.generate_step()

        if res:
            self.new_file = False
            self.action, self.file_paths, self.current_snippets, self.new_file = res

            if len(self.file_paths) > 0:
                print_files = [env.relative_path(f) for f in self.file_paths]
                self.app.call_from_thread(self.fume_print, f"Working on {', '.join(print_files)}")
            else:
                self.app.call_from_thread(self.fume_print, f"Working on {env.relative_path(self.file_paths[0])}")

            self.app.call_from_thread(self.fume_print, content=self.action)

            self.app.call_from_thread(self.fume_print, content='Does this plan look good to you?')

            self.answer_actions = [self.apply_plan, self.get_feedback, self.edit_plan]
            self.app.call_from_thread(self.ask_multi_choice, options=['Yes', 'No', 'Edit'])

        else:
            self.app.call_from_thread(self.disableContextEditButtons)
            self.app.call_from_thread(self.fume_print, "I decided the task is done.")
            env.posthog.capture(env.USER_ID, event='task_done', properties={'task': env.TASK, 'task_id': env.TASK_ID})
            self.app.call_from_thread(self.fume_print, "What's next?")
            self.app.call_from_thread(self.ask_open_ended, action=self.solve_task)

    async def apply_plan(self):
        self.app.call_from_thread(self.start_loading)
        self.app.call_from_thread(self.fume_print, content="I will continue with this plan")

        new_snippets = [snippet for snippet in env.SNIPPETS if not snippet.get('file_path') in self.file_paths]
        env.SNIPPETS = new_snippets

        if len(self.file_paths) > 1:
            print_files = ', '.join([env.relative_path(f) for f in self.file_paths])
        else:
            print_files = env.relative_path(self.file_paths[0])

        if self.new_file:
            self.diffs.append(f"* You created {print_files}. Here is what you did:\n{self.action}")
            CoderMinion(task=self.action, file_paths=self.file_paths).create_file()
            self.run_worker(self.start_philly(), thread=True)
            return

        changes = if_changes_needed(speech=self.action)

        decision = changes.get('decision')
        is_multiple = changes.get('is_multiple')

        if decision:
            self.diffs.append(f"* You modified {print_files}. Here is what you did:\n{self.action}")
            if is_multiple:

                old_files = []
                for path in self.file_paths:
                    with open(path, 'r') as file:
                        old_files.append(file.read())

                self.app.call_from_thread(self.fume_print, 'Preparing the steps')
                sub_tasks_dict = split_complex_task(self.action)

                sub_tasks = sub_tasks_dict.get('plan')
                for t in sub_tasks:

                    task = '# ' + t.get('task') + '\n' + '* ' + '\n'.join(t.get('steps'))

                    coder = CoderMinion(task=task, file_paths=self.file_paths)
                    self.app.call_from_thread(self.fume_print, f'Writing the code for {task}')
                    coder.code()

            else:
                new_snippets = [snippet for snippet in env.SNIPPETS if not snippet.get('file_path') in self.file_paths]
                env.SNIPPETS = new_snippets

                old_files = []
                for path in self.file_paths:
                    with open(path, 'r') as file:
                        old_files.append(file.read())

                # Assuming 'action' is defined elsewhere and appropriate for 'task'
                coder = CoderMinion(task=self.action, file_paths=self.file_paths)
                self.app.call_from_thread(self.fume_print, content='Writing the code...')
                coder.code()

        else:
            for path in self.file_paths:
                relative_path = env.relative_path(path)
                self.diffs.append('# ' + relative_path + '\n' + self.action)

        self.run_worker(self.start_philly(), thread=True)

    async def get_feedback(self):
        self.app.call_from_thread(self.fume_print, 'Can you tell me what I should change about the plan?')
        self.app.call_from_thread(self.ask_open_ended, action=self.apply_feedback)

    async def exit_with_message(self):
        self.notify('Please change to the correct directory using cd command.', severity='error')
        await asyncio.sleep(5)  # Wait for 5 seconds
        self.app.exit()

    async def apply_feedback(self):
        feedback = self.latest_user_input

        self.app.call_from_thread(self.start_loading)

        processed_snippets = process_snippets(snippets=env.SNIPPETS)         
        phil = Philosopher(task=env.TASK, snippets=processed_snippets, short_snippets=env.SNIPPETS)

        self.app.call_from_thread(self.fume_print, content='Thinking about how to apply the feedback')
        res = phil.apply_feedback(action=self.action, feedback=feedback, file_path=self.file_paths, current_snippets=self.current_snippets)

        if res:
            self.new_file = False
            self.action, self.file_paths, self.current_snippets, self.new_file = res
        else:
            self.app.call_from_thread(self.disableContextEditButtons)
            self.app.call_from_thread(self.fume_print, "I decided the task is done.")
            env.posthog.capture(env.USER_ID, event='task_done', properties={'task': env.TASK,'task_id':env.TASK_ID})
            self.app.call_from_thread(self.fume_print, "What's next?")
            self.app.call_from_thread(self.ask_open_ended, action=self.solve_task)

        self.app.call_from_thread(self.fume_print, self.action)

        self.answer_actions = [self.apply_plan, self.get_feedback]
        self.app.call_from_thread(self.fume_print, content='Is the plan good now?')
        self.app.call_from_thread(self.ask_multi_choice, options=['Yes', 'No'])

    async def edit_plan(self):
        self.app.call_from_thread(self.ask_open_ended, value=self.action, action=self.apply_edited_plan)

    async def apply_edited_plan(self):
        self.action = self.latest_user_input
        self.app.call_from_thread(self.fume_print, content="Appyling your edited plan")
        self.run_worker(self.apply_plan(), thread=True)

    def on_mount(self):
        try:
            self.run_worker(self.check_project(), thread=True)
        except Exception as e:
            sentry_sdk.capture_exception(e)


    async def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id.startswith('answer'):
            answer_idx = int(button_id.replace('answer', ''))
            self.run_worker(self.answer_actions[answer_idx](), thread=True)

        elif button_id == 'submit':
            user_input = self.query_one("#userInput")
            self.user_print(content=user_input.text)
            self.latest_user_input = user_input.text
            user_input.text = ""
            self.run_worker(self.open_ended_action(), thread=True)

    def compose(self) -> ComposeResult:
        yield Container(ChatWindow(id="chatWindow"), ContextFiles(context=self.context), id="container")