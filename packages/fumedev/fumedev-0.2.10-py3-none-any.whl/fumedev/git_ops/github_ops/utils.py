from datetime import datetime, timezone
from dotenv import load_dotenv
import requests
import sentry_sdk

load_dotenv(override=True)
from github import Github
from fumedev import env


def create_github_pr(head_branch, base_branch, pr_title, pr_body):
    # Your GitHub token and repository details

    # Branch details
    HEAD_BRANCH = head_branch
    BASE_BRANCH = base_branch

    # PR details
    PR_TITLE = pr_title
    PR_BODY = pr_body

    # Initialize GitHub client
    g = Github(env.get_github_token())

    # Get the repository
    repo = g.get_repo(env.REPO_NAME)

    # Create a pull request
    try:
        pr = repo.create_pull(title=PR_TITLE, body=PR_BODY, head=HEAD_BRANCH, base=BASE_BRANCH)
        print(f'Pull request created successfully at {pr.html_url}')
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f'Failed to create pull request: {e}')

def get_repo_id(repo_name):

    g = Github(env.get_github_token())

    repo = g.get_repo(repo_name)

    return repo.id


# Function to get commits from a pull request
def get_pr_modified_files(pr_id):
    g = Github(env.get_github_token())
    repo = g.get_repo(env.REPO_NAME)
    pr = repo.get_pull(pr_id)
    commits = pr.get_commits()
    modified_files = []
    for commit in commits:
        files = commit.files
        for file in files:
            modified_files.append('./codebase/'+file.filename)
    return list(set(modified_files))



def get_pr_head(pr_number):
    g = Github(env.get_github_token())
    repo = g.get_repo(env.REPO_NAME)
    pr = repo.get_pull(pr_number)
    return pr.head.ref





def pr_comment(pr_number, comment):
    g = Github(env.get_github_token())
    repo = g.get_repo(env.REPO_NAME)
    pr = repo.get_pull(pr_number)
    pr.create_issue_comment(comment)
    

def get_github_isssues():
    # Initialize Github instance with the token
    g = Github(env.get_github_token())

    # Access the repository
    repo = g.get_repo(env.REPO_NAME)

    # Retrieve all projects in the repository
    projects = repo.get_projects()
    project_data = []

    # Iterate through each project
    for project in projects:
        project_info = {
            "project_name": project.name,
            "columns": []
        }

        # Retrieve columns in the project
        columns = project.get_columns()
        for column in columns:
            column_info = {
                "column_name": column.name,
                "cards": []
            }

            # Retrieve cards in the column
            cards = column.get_cards()
            for card in cards:
                card_info = {}
                if card.get_content() is not None:
                    content = card.get_content()
                    card_info["type"] = "issue" if content.__class__.__name__ == "Issue" else "pull_request"
                    card_info["title"] = content.title
                    card_info["url"] = content.html_url
                else:
                    card_info["type"] = "note"
                    card_info["note"] = card.note

                column_info["cards"].append(card_info)

            project_info["columns"].append(column_info)

        project_data.append(project_info)

    return project_data

def get_pr_body(pr_number):
    g = Github(env.get_github_token())
    repo = g.get_repo(env.REPO_NAME)
    pr = repo.get_pull(pr_number)
    return pr.body

def get_pr_diff(pr_number):    
    diff_url = f'https://api.github.com/repos/{env.REPO_NAME}/pulls/{pr_number}.diff'

    headers = {
        'Authorization': f'token {env.get_github_token()}',
        'Accept': 'application/vnd.github.v3.diff'
               }
    response = requests.get(diff_url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch the diff: ", response.status_code)
        return False
    


def get_last_commit_time_of_pr(pr_number):
    """
    Fetch the time of the last commit of a pull request on GitHub.

    :param pr_number: The pull request number
    :param token: Personal access token for GitHub (if needed)
    :return: The time of the last commit or None if not found
    """

    # GitHub API URL for the pull request commits
    url = f"https://api.github.com/repos/{env.REPO_NAME}/pulls/{pr_number}/commits"

    # Set up headers for authentication if a token is provided
    headers = {"Authorization": f"token {env.get_github_token()}"}

    # Make the request to the GitHub API
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        commits = response.json()

        # Check if there are any commits in the PR
        if commits:
            # The last commit is the last item in the list
            last_commit = commits[-1]
            last_commit_date_str = last_commit['commit']['committer']['date']

            # Convert to datetime object
            datetime_obj = datetime.fromisoformat(last_commit_date_str.replace("Z", "+00:00"))


            # Convert to Unix timestamp
            unix_timestamp = datetime_obj.replace(tzinfo=timezone.utc).timestamp()
            return unix_timestamp
        else:
            print("No commits found in this pull request.")
            return None
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None
    
def reply_to_pr_review_comment(pr_number, review_comment_id, reply_message):
    """
    Reply to a pull request review comment on GitHub.

    :param pr_number: Pull request number
    :param comment_id: ID of the comment to reply to
    :param reply_message: The reply message
    """
    # Authenticate with GitHub
    url = f'https://api.github.com/repos/{env.REPO_NAME}/pulls/{pr_number}/comments/{review_comment_id}/replies'


    headers = {
    'Authorization': f'token {env.get_github_token()}',
    'Accept': 'application/vnd.github.v3+json'
    }

    # Data
    data = {
    'body': reply_message
    }

    response = requests.post(url, json=data, headers=headers).json()

    reply_id = response.get('id')

    return reply_id


def get_github_review_comment_replies(pr_number, comment_id):
    """
    Fetches all replies to a specific review comment in a GitHub pull request.

    :param token: GitHub Personal Access Token (PAT)
    :param repo_name: Repository name including the owner (e.g., 'owner/repo')
    :param pull_number: Pull request number
    :param comment_id: ID of the review comment
    :return: List of replies to the review comment
    """
    g = Github(env.get_github_token())
    repo = g.get_repo(env.REPO_NAME)
    pull_request = repo.get_pull(pr_number)
    comments = pull_request.get_review_comments()

    replies = []
    for comment in comments:
        if comment.id == comment_id:
            # Fetching the replies for the specific comment
            replies = comment.get_replies()
            break

    return [reply.body for reply in replies]


def add_github_pr_comment(pr_number, comment_body):
    """
    Add a comment to a GitHub pull request and return the new comment's ID.

    :param token: GitHub Personal Access Token
    :param repo_owner: Owner of the repository (username or organization)
    :param repo_name: Name of the repository
    :param pr_number: Number of the pull request
    :param comment_body: The content of the comment
    :return: ID of the created comment
    """
    url = f"https://api.github.com/repos/{env.REPO_NAME}/issues/{pr_number}/comments"
    
    headers = {
        "Authorization": f"token {env.get_github_token()}",
        "Accept": "application/vnd.github.v3+json"
    }

    data = {
        "body": comment_body
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return response.json()['id']
    else:
        raise Exception(f"Failed to add comment: {response.json()}")

def get_pr_author(pr_number):
    """
    Get the author of a pull request on GitHub.
    Parameters:
    pr_number (int): The number of the pull request.
    Returns:
    str: The username of the pull request author.
    """
    url = f"https://api.github.com/repos/{env.REPO_NAME}/pulls/{pr_number}"
    headers = {'Authorization': f'token {env.get_github_token()}'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        pr_data = response.json()
        return pr_data.get('user', {}).get('login')
    else:
        return "Error: Unable to fetch PR details"
    

def get_pr_comments_after_timestamp(pr_number, timestamp):
    """
    Fetch comments on a pull request after a specific Unix timestamp.


    :param pr_number: The pull request number
    :param timestamp: The Unix timestamp (number of seconds since Jan 1, 1970)
    :return: A list of comments made after the specified timestamp
    """
    # Initialize GitHub client with token
    g = Github(env.get_github_token())

    # Get the repository and pull request objects
    repo = g.get_repo(env.REPO_NAME)
    pr = repo.get_pull(pr_number)

    # Fetch and filter comments
    comments_after_timestamp = []
    for comment in pr.get_issue_comments():
        comment_unix_timestamp = int(comment.created_at.timestamp())
        if comment_unix_timestamp > timestamp:
            comments_after_timestamp.append(comment)

    return comments_after_timestamp


def get_authenticated_user_details():
    """
    Fetch the details of the authenticated GitHub user.

    Args:
    access_token (str): Your GitHub personal access token.

    Returns:
    dict: A dictionary containing the authenticated user's GitHub details.
    """
    url = "https://api.github.com/user"
    headers = {'Authorization': f'token {env.get_github_token()}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Returns the user details as a dictionary
    else:
        return {'error': 'Unable to fetch user details', 'status_code': response.status_code}



def get_authenticated_user_details():
    """
    Fetch the details of the authenticated GitHub user.

    Args:
    access_token (str): Your GitHub personal access token.

    Returns:
    dict: A dictionary containing the authenticated user's GitHub details.
    """
    url = "https://api.github.com/user"
    headers = {'Authorization': f'token {env.get_github_token()}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Returns the user details as a dictionary
    else:
        print({'error': 'Unable to fetch user details', 'status_code': response.status_code, 'response': response.text})
    

def get_pr_object(pr_number):
    """
    Retrieve a Pull Request object from GitHub.

    Parameters:
    pr_id (int): The ID of the Pull Request.

    Returns:
    github.PullRequest.PullRequest: The Pull Request object.
    """
    # Authenticate with GitHub
    g = Github(env.get_github_token())

    # Get the repository
    repo = g.get_repo(env.REPO_NAME)

    # Get the Pull Request
    pr = repo.get_pull(pr_number)

    return pr


def get_github_prs_by_state(state='open'):
    """
    Fetch all pull requests from a GitHub repository that matches the given state.

    Returns:
    dict: A dictionary containing pull requests with the given state
    """
    # Initialize GitHub client with token
    g = Github(env.get_github_token())
    repo = g.get_repo(env.REPO_NAME)

    # Fetch pull requests with the given state
    prs = repo.get_pulls(state=state)
    return prs

