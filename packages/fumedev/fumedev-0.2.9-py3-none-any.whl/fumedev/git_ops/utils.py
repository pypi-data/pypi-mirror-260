import os
import random
import shutil
import time
from git import Actor, GitCommandError, RemoteProgress, Repo
import git
from fumedev import env



def pull_repo ():
    
    if env.REPO_SERVICE == 'GITHUB':
        repo_url = f'https://x-access-token:{env.get_github_token()}@github.com/{env.REPO_NAME}.git'
    elif env.REPO_SERVICE == 'GITLAB':
        repo_url = f'https://{env.GITLAB_USERNAME}:{env.GITLAB_TOKEN}@{env.GITLAB_DOMAIN}/{env.REPO_NAME}.git'

    LOCAL_PATH = env.absolute_path('codebase')

    #DELETE THE LOCAL REPO
    if os.path.exists(LOCAL_PATH):
        shutil.rmtree(LOCAL_PATH)

    os.makedirs(LOCAL_PATH)

    try:
        Repo.clone_from(repo_url, LOCAL_PATH)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e

def commit_changes (commit_message):
    REPO_PATH = env.absolute_path('codebase')
    # Initialize the repository object
    repo = Repo(REPO_PATH)

    try:
        # Check if there are any changes
        if repo.is_dirty(untracked_files=True):
            # Add all changes to the staging area
            repo.git.add(all=True)

            bot_actor = Actor('FumeDev', 'FumeDev@users.noreply.github.com')

            # Commit changes
            repo.index.commit(commit_message,author=bot_actor,committer=bot_actor)
            print('Changes committed successfully.')
        else:
            print('No changes to commit.')

    except GitCommandError as error:
        print(f'Error occurred while committing: {error}')


def push_code():
    REPO_PATH = env.absolute_path('codebase')

    if env.REPO_SERVICE == 'GITHUB':
        repo_url = f'https://x-access-token:{env.get_github_token()}@github.com/{env.REPO_NAME}.git'
    elif env.REPO_SERVICE == 'GITLAB':
        repo_url = f'https://{env.GITLAB_USERNAME}:{env.GITLAB_TOKEN}@gitlab.com/{env.REPO_NAME}.git'

    try:
        # Initialize the repository object
        repo = Repo(REPO_PATH)
        origin = repo.remote(name='origin')
        origin.set_url(repo_url)

        # Get the current branch name
        current_branch = repo.active_branch.name

        # Check if the current branch has an upstream branch
        if not repo.active_branch.tracking_branch():
            # Set the upstream branch if not set
            origin.push(refspec=f'{current_branch}:{current_branch}', set_upstream=True)
            print(f"Upstream set for branch '{current_branch}'. Changes pushed to remote repository.")
        else:
            # Push changes to remote repository
            origin.push()
            print('Changes pushed successfully.')

    except GitCommandError as error:
        print(f'Error occurred: {error}')


def create_branch(branch_name):
    # Replace this with the path to your local git repository
    REPO_PATH = env.absolute_path('codebase')

    # Replace this with the name of the new branch you want to create
    NEW_BRANCH_NAME = branch_name

    try:
        # Initialize the repository object
        repo = Repo(REPO_PATH)

        # Check if the branch already exists
        if NEW_BRANCH_NAME in repo.heads:
            print(f"Branch '{NEW_BRANCH_NAME}' already exists.")
        else:
            # Create a new branch
            new_branch = repo.create_head(NEW_BRANCH_NAME)

            # Checkout the new branch
            new_branch.checkout()
            print(f"Switched to new branch '{NEW_BRANCH_NAME}'.")

            # Push the new branch to remote
            origin = repo.remote(name='origin')
            origin.push(refspec=f'{NEW_BRANCH_NAME}:{NEW_BRANCH_NAME}')
            print(f"Branch '{NEW_BRANCH_NAME}' has been published to the remote repository.")

    except GitCommandError as error:
        print(f'Error occurred: {error}')


def move_to_branch(branch_name):
    REPO_PATH = env.absolute_path('codebase')
    # Initialize the repository object
    repo = Repo(REPO_PATH)

    # Get the current branch name
    current_branch = repo.active_branch.name
    origin = repo.remote(name='origin')

    # Check if the current branch is the same as the branch we want to move to
    if current_branch == branch_name:
        print(f'Already on branch {branch_name}.')
    else:
        try:
            # Fetch from remote first
            origin.fetch()

            # If the branch exists locally
            if branch_name in repo.heads:
                branch = repo.heads[branch_name]
                # Hard reset to the state of remote branch and checkout with force
                branch.checkout(force=True)
                repo.git.reset('--hard', f'origin/{branch_name}')
                print(f'Switched to branch {branch_name} with force. Local changes have been discarded.')
            else:
                # If the branch doesn't exist locally but exists on remote
                try:
                    repo.create_head(branch_name, origin.refs[branch_name])
                    repo.heads[branch_name].set_tracking_branch(origin.refs[branch_name])
                    repo.heads[branch_name].checkout(force=True)
                    repo.git.reset('--hard', f'origin/{branch_name}')
                    print(f'Created and switched to local branch {branch_name} with force. Local changes have been discarded.')
                except IndexError:
                    print(f'Branch {branch_name} does not exist on the remote.')
                    return
                
            

            # Pull the latest changes from the remote
            try:
                origin.pull(branch_name)
                print(f'Pulled latest changes for branch {branch_name} from remote {origin.url}.')
            except GitCommandError as e:
                print(f'Failed to pull changes for branch {branch_name}. Error: {e}')
                raise e
        except GitCommandError as e:
            print(f'Error while switching to branch {branch_name}. Error: {e}')
        

def create_stash():
    repo_path = env.absolute_path('codebase')
    try:
        repo = Repo(repo_path)
        # Create a unique tag name using a combination of current time and a random number
        tag_name = f"stash-{int(time.time())}-{random.randint(1000, 9999)}"

        # Stash changes with a unique message
        stash_ref = repo.git.stash('save', f"Stash for tag {tag_name}")

        # Get the commit hash of the new stash
        stash_commit = repo.git.rev_parse('stash@{0}')

        # Create a tag for this stash
        repo.create_tag(tag_name, ref=stash_commit)
        return tag_name
    except git.exc.GitCommandError as e:
        return f"Git command error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def apply_git_stash(tag_name):
    repo_path = env.absolute_path('codebase')
    try:
        repo = Repo(repo_path)

        # Check if the tag exists
        if tag_name not in repo.tags:
            return f"Tag {tag_name} not found."

        # Get the commit associated with the tag
        stash_commit = repo.tags[tag_name].commit

        # Apply the stash
        repo.git.stash('apply', stash_commit)
        return f"Stash with tag {tag_name} applied successfully."
    except git.exc.GitCommandError as e:
        return f"Git command error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def get_git_diff():
    repo_path = env.absolute_path('codebase')
    try:
        # Initialize the repository object
        repo = Repo(repo_path)

        # Check if the repository has any uncommitted changes
        if repo.is_dirty(untracked_files=True):
            # Get the diff of the working directory
            diff = repo.git.diff(None)
            return diff
        else:
            return "No changes detected."
    except git.exc.InvalidGitRepositoryError:
        return "Invalid Git repository."
    except Exception as e:
        return f"An error occurred: {e}"
    
def undo_local_commits_but_keep_changes(repo_path=env.absolute_path('codebase')):
    repo = Repo(repo_path)
    origin = repo.remotes.origin
    origin.fetch()  # Fetch latest changes from the remote

    current_branch = repo.active_branch.name
    remote_commit = origin.refs[current_branch].commit  # Get the commit to reset to, typically origin/master or origin/main

    # Reset to the remote commit but keep local changes unstaged
    repo.git.reset(remote_commit)

    print(f"Commits undone. Current branch '{current_branch}' is now at {remote_commit.hexsha}, with local changes kept unstaged.")
    



