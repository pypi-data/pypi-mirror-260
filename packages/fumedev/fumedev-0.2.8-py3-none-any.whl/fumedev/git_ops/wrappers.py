from fumedev import env
from git_ops.gitlab_ops import utils as gitlab_utils
from git_ops.github_ops import utils as github_utils

def get_pr_head(pr_number):
    if env.REPO_SERVICE == 'GITHUB':
        return github_utils.get_pr_head(pr_number)  # Replace with actual GitHub function
    elif env.REPO_SERVICE == 'GITLAB':
        return gitlab_utils.get_mr_head(pr_number)  # Replace with actual GitLab function

# Wrapper function for getting modified files in a pull/merge request
def get_pr_modified_files(pr_id):
    if env.REPO_SERVICE == 'GITHUB':
        return github_utils.get_pr_modified_files(pr_id)  # Replace with actual GitHub function
    elif env.REPO_SERVICE == 'GITLAB':
        return gitlab_utils.get_mr_modified_files(pr_id)  # Replace with actual GitLab function



# Wrapper function for creating a pull/merge request
def create_pr(head_branch, base_branch, pr_title, pr_body):
    if env.REPO_SERVICE == 'GITHUB':
        return github_utils.create_github_pr(head_branch, base_branch, pr_title, pr_body)  # Replace with actual GitHub function
    elif env.REPO_SERVICE == 'GITLAB':
        return gitlab_utils.create_mr(head_branch, base_branch, pr_title, pr_body)  # Replace with actual GitLab function

# Wrapper function for getting the repository ID
def get_repo_id(repo_name):
    if env.REPO_SERVICE == 'GITHUB':
        return github_utils.get_repo_id(repo_name)  # Replace with actual GitHub function
    elif env.REPO_SERVICE == 'GITLAB':
        return gitlab_utils.get_gitlab_repo_id(repo_name)  # Replace with actual GitLab function

# Wrapper function for adding a comment to a pull/merge request
def pr_comment(pr_number, comment):
    if env.REPO_SERVICE == 'GITHUB':
        return github_utils.pr_comment(pr_number, comment)  # Replace with actual GitHub function
    elif env.REPO_SERVICE == 'GITLAB':
        return gitlab_utils.mr_comment(pr_number, comment)  # Replace with actual GitLab function

# Wrapper function for getting the body of a pull/merge request
def get_pr_body(pr_number):
    if env.REPO_SERVICE == 'GITHUB':
        return github_utils.get_pr_body(pr_number)  # Replace with actual GitHub function
    elif env.REPO_SERVICE == 'GITLAB':
        return gitlab_utils.get_mr_description(pr_number)  # Replace with actual GitLab function

# Wrapper function for getting the diff of a pull/merge request
def get_pr_diff(pr_number):    
    if env.REPO_SERVICE == 'GITHUB':
        return github_utils.get_pr_diff(pr_number)  # Replace with actual GitHub function
    elif env.REPO_SERVICE == 'GITLAB':
        return gitlab_utils.get_mr_diff(pr_number)  # Replace with actual GitLab function

# Wrapper function for getting pull/merge request reviews
def get_pr_reviews():
    if env.REPO_SERVICE == 'GITHUB':
        return github_utils.get_pr_reviews() # Replace with actual GitHub function
    elif env.REPO_SERVICE == 'GITLAB':
        return gitlab_utils.get_mr_reviews() # Replace with actual GitLab function
    
def get_prs_by_state(state):
    if env.REPO_SERVICE == 'GITHUB':
        return github_utils.get_github_prs_by_state(state) # Replace with actual GitHub function
    elif env.REPO_SERVICE == 'GITLAB':
        return gitlab_utils.get_mrs_by_state(state) # Replace with actual GitLab function
