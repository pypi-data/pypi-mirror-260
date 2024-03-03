import os
from pathlib import Path
import time

from dotenv import load_dotenv
from posthog import Posthog
load_dotenv()

posthog = Posthog(project_api_key='phc_4XYWzMZgroHVOWIu8Qfa9UTql93LxaXps6AfGmuzcC8', host='https://app.posthog.com')
USER_ID = None
TASK_ID = None
CLOUD_HOSTED = os.getenv("CLOUD_HOSTED",'').lower() == 'true'
USER_HOME_PATH = Path.home()
BASE_MODEL = 'gpt-4-0125-preview'
BASE_URL = 'https://llm-proxy.fumedev.com'
if CLOUD_HOSTED:
    BASE_URL = 'https://api.openai.com/v1'
PROJECT_PATH = "../codebase"
EXCLUDE_DIRS = '__pycache__,.git,.idea,.vscode,node_modules,venv,build,dist,env,lib,bin,logs,log'
EXCLUDE_FILES = 'LICENSE,README.md,.gitignore,.DS_Store,.env,.env.example,.gitattributes,.gitmodules,.gitkeep,.git,package-lock.json,package.json,requirements.txt,setup.cfg,pyproject.toml,poetry.lock,poetry.toml'
EXCLUDE_FOLDERS = ['env', 'node_modules', 'cache']
NONTRVIVIAL_FILES = ['js', 'html', 'py', 'css', 'go', 'java', 'ts', 'tsx', 'c', 'cpp', 'cs', 'php', 'rb', 'rs', 'swift', 'pug','tcss']
OPENAI_API_KEY = ''
FILE_FOLDER = ''
SNIPPETS = []
TASK = ''
CHAT_LOG = []

COHERE_API_KEY = "gGrZ0s7J7xx6qbVrfJwz8wBBoTjC1dRCRxR1Zp1N"
SLACK_CLIENT_ID = os.getenv('SLACK_CLIENT_ID')
SLACK_CLIENT_SECRET = os.getenv('SLACK_CLIENT_SECRET')
SLACK_SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

REPO_SERVICE = os.getenv("REPO_SERVICE")
ORG_NAME = os.getenv("ORG_NAME")
GITHUB_APP_ID = os.getenv("GITHUB_APP_ID")
GITHUB_PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH")
GITLAB_USERNAME = os.getenv("GITLAB_USERNAME")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
GITLAB_DOMAIN = os.getenv("GITLAB_DOMAIN")
REPO_NAME = os.getenv("REPO_NAME")
GITHUB_PAT = os.getenv("GITHUB_PAT")
base_branch = os.getenv("BASE_BRANCH")
GITHUB_TOKEN = {
    'TOKEN':'',
    'EXPIRTATION':None
}
SLACK_REDIRECT_HOST= os.getenv("SLACK_REDIRECT_HOST")

GITHUB_APP = None

IS_WORKING = False

def get_github_token():
    if CLOUD_HOSTED:
        if GITHUB_TOKEN['EXPIRTATION'] and GITHUB_TOKEN['EXPIRTATION'] > time.time():
            return GITHUB_TOKEN['TOKEN']
        else:
            #Get new token
            GITHUB_APP.fetch_installation_access_token()
            return GITHUB_TOKEN['TOKEN']
    else:
        return GITHUB_PAT

def absolute_path(path):
    file_path = str(USER_HOME_PATH) + '/FumeData/' + path
    return file_path

def relative_path(path):
    # Remove the user's home path and FumeData directory from the beginning of the path
    # Do not modify the original path
    return path.replace(str(USER_HOME_PATH) + '/FumeData/', '')


def parse_gitignore():
    project_path = Path(PROJECT_PATH)  # Leveraging the existing PROJECT_PATH variable
    gitignore_path = project_path / '.gitignore'  # Constructing the full path to .gitignore
    global EXCLUDE_FILES, EXCLUDE_FOLDERS  # To modify the global variables

    if gitignore_path.exists():
        with gitignore_path.open('r') as f:
            for line in f:
                stripped_line = line.strip()
                # Ignoring empty lines and comments
                if stripped_line and not stripped_line.startswith('#'):
                    if stripped_line.endswith('/') and 'codebase' not in stripped_line:
                        # It's a directory, excluding the trailing slash for consistency
                        EXCLUDE_FOLDERS.append(stripped_line[:-1])
                    else:
                        # It's a file
                        EXCLUDE_FILES += ',' + stripped_line
    else:
        print("Warning: .gitignore file not found at", gitignore_path)

def append_hidden_folders_to_exclude():
    project_path = Path(PROJECT_PATH)
    for item in project_path.iterdir():
        if item.is_dir() and item.name.startswith('.'):
            if item.name not in EXCLUDE_FOLDERS:
                EXCLUDE_FOLDERS.append(item.name)
