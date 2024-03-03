from openai import OpenAI
from fumedev.git_ops.utils import commit_changes, create_branch, push_code
from fumedev.git_ops.wrappers import create_pr, pr_comment
from fumedev import env

sample_branch_name = 'pagination_for_earth_api'
sample_pr_title = 'Appended the documentation to Readme.md'
sample_pr_body = """
CHANGED
- Changed the User model to add habits field, which is an array of ObjectIds that represent the habits selected by the specific user.
"""

def submit_code(plan):

    branch_name = create_branch_name(plan=plan)
    try:
        create_branch(branch_name=branch_name)
    except Exception as e:
        print('Failed to create branch: ' + branch_name)
        print(e)
        return False
    print('Branch created successfully: ' + branch_name)

    commit_message = create_commit_message(plan=plan)
    commit_changes(commit_message=commit_message)
    print('Created a commit: ' + commit_message)
    push_code()

    pr_title = create_pr_title(plan=plan)
    pr_body = create_pr_body(plan=plan)

    create_pr(head_branch=branch_name, base_branch=env.base_branch, pr_title=pr_title, pr_body=pr_body)
    return True


def create_branch_name(plan):
    client = OpenAI(base_url=env.BASE_URL, api_key=env.OPENAI_API_KEY)
    prompt = f""""
    Given a plan for a task, your job is to come up with a Git branch name for it.
    Your branch name should be concise but descriptive.
    Here is an example branch name:
    {sample_branch_name}
    Try to adhere to the format of the sample branch name.
    """

    user_message = f"""
    Plan: {plan}
    """

    messages = [{'role': 'system', 'content': prompt}, {'role': 'user', 'content': user_message}]

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages
    )

    response_message = response.choices[0].message.content
    return response_message

def create_commit_message (plan):
    client = OpenAI(base_url=env.BASE_URL, api_key=env.OPENAI_API_KEY)
    prompt = f""""
    Given a completed plan, your job is to come up with a Git commit message for it.
    Your commit message should be concise but descriptive.
    Your answer should be 1 short commmit message describing the overall of the steps.
    """

    user_message = f"""
    Completed Plan: {plan}
    """

    messages = [{'role': 'system', 'content': prompt}, {'role': 'user', 'content': user_message}]

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages
    )

    response_message = response.choices[0].message.content
    return response_message

def create_pr_title (plan):
    client = OpenAI(base_url=env.BASE_URL, api_key=env.OPENAI_API_KEY)
    prompt = f""""
    Given a completed plan for a task, your job is to come up with a Git PR Title for it.
    Your title should be concise but descriptive.
    Your answer should be 1 title describing the overall of the steps.
    Here is a sample PR Title:
    {sample_pr_title}
    Try to adhere to the sample format as much as possible.
    """

    user_message = f"""
    Completed Plan: {plan}
    """

    messages = [{'role': 'system', 'content': prompt}, {'role': 'user', 'content': user_message}]

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages
    )

    response_message = response.choices[0].message.content
    return response_message

def create_pr_body (plan):
    client = OpenAI(base_url=env.BASE_URL, api_key=env.OPENAI_API_KEY)
    prompt = f""""
    Given a completed plan for a task, your job is to come up with a Git PR Body for it.
    Your body should be descriptive of the stuff done in the plan.
    Your answer should be 1 body text.
    Here is a sample PR Body:
    {sample_pr_body}
    Try to adhere to the sample format as much as possible.
    """

    user_message = f"""
    Completed Plan: {plan}
    """

    messages = [{'role': 'system', 'content': prompt}, {'role': 'user', 'content': user_message}]

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages
    )

    response_message = response.choices[0].message.content
    return response_message

def create_issue_comment(feedback,plan):
    client = OpenAI(base_url=env.BASE_URL, api_key=env.OPENAI_API_KEY)
    prompt = f""""
    You are given a feedback for a previous task you submitted and plan you came up with to adress the issues in the feedback.
    Your job is to come up with a Git new issue comment.
    Your body should be descriptive of the stuff done in the plan.
    Your answer should be 1 body text.
    Here is a sample PR Body:
    {sample_pr_body}
    Try to adhere to the sample format as much as possible.
    """

    user_message = f"""
    Feedback: {feedback} 
    Completed Plan: {plan}
    """

    messages = [{'role': 'system', 'content': prompt}, {'role': 'user', 'content': user_message}]

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages
    )

    response_message = response.choices[0].message.content
    return response_message


def create_commmit_message_from_diff(diff_string):
    client = OpenAI(base_url=env.BASE_URL, api_key=env.OPENAI_API_KEY)
    prompt = f""""
    Given a diff, your job is to come up with a Git commit message for it.
    Your commit message should be concise but descriptive.
    Your answer should be 1 short commmit message describing the overall of the steps.
    """

    user_message = f"""
    Diff: {diff_string}
    """

    messages = [{'role': 'system', 'content': prompt}, {'role': 'user', 'content': user_message}]

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages
    )

    response_message = response.choices[0].message.content
    return response_message


