import json
import os
from dotenv import load_dotenv
import gitlab
import requests
from fumedev import env
load_dotenv(override=True)



def get_mr_head(mr_number):
    
    # Create a GitLab instance
    gl = gitlab.Gitlab(f'https://{env.GITLAB_DOMAIN}', private_token=env.GITLAB_TOKEN)
    
    # Get the project
    project = gl.projects.get(env.REPO_NAME)

    # Get the merge request
    mr = project.mergerequests.get(mr_number)

    # Return the source branch name of the merge request
    return mr.source_branch

def get_mr_modified_files(mr_id):
    # Initialize a GitLab instance
    gl = gitlab.Gitlab(f'https://{env.GITLAB_DOMAIN}', private_token=env.GITLAB_TOKEN)

    # Get the project
    project = gl.projects.get(env.REPO_NAME)

    # Get the merge request
    mr = project.mergerequests.get(mr_id)

    # Initialize a list to hold paths of modified files
    modified_files = []

    # Iterate over each commit in the merge request
    for commit in mr.commits():
        # Get detailed information about the commit
        detailed_commit = project.commits.get(commit.get_id())
        
        # Iterate over each changed file in the commit
        for file in detailed_commit.diff():
            modified_files.append('./codebase/' + file['new_path'])

    return modified_files

def create_mr(head_branch, base_branch, mr_title, mr_body):
    # Initialize GitLab client
    gl = gitlab.Gitlab(f'https://{env.GITLAB_DOMAIN}', private_token=env.GITLAB_TOKEN)

    # Get the repository (project in GitLab terms)
    project = gl.projects.get(env.REPO_NAME)

    # Create a merge request
    try:
        mr = project.mergerequests.create({
            'source_branch': head_branch,
            'target_branch': base_branch,
            'title': mr_title,
            'description': mr_body
        })
        print(f'Merge request created successfully at {mr.web_url}')
    except Exception as e:
        print(f'Failed to create merge request: {e}')


def get_gitlab_repo_id(repo_name):
    # Initialize GitLab client
    gl = gitlab.Gitlab(f'https://{env.GITLAB_DOMAIN}', private_token=env.GITLAB_TOKEN)

    # Get the repository (project in GitLab terms)
    project = gl.projects.get(repo_name)

    return project.get_id()

def mr_comment(mr_number, comment):
    # Initialize GitLab client
    gl = gitlab.Gitlab(f'https://{env.GITLAB_DOMAIN}', private_token=env.GITLAB_TOKEN)

    # Get the project
    project = gl.projects.get(env.REPO_NAME)

    # Get the merge request
    mr = project.mergerequests.get(mr_number)

    # Create a comment on the merge request
    mr.notes.create({'body': comment})

def get_mr_description(mr_number):
    # Initialize GitLab client
    gl = gitlab.Gitlab(f'https://{env.GITLAB_DOMAIN}', private_token=env.GITLAB_TOKEN)

    # Get the project
    project = gl.projects.get(env.REPO_NAME)

    # Get the merge request
    mr = project.mergerequests.get(mr_number)

    # Return the description of the merge request
    return mr.description


def get_mr_diff(mr_number):

    project_id = get_gitlab_repo_id(env.REPO_NAME)
    diff_url = f'https://{env.GITLAB_DOMAIN}/api/v4/projects/{project_id}/merge_requests/{mr_number}/changes'

    headers = {
        'PRIVATE-TOKEN': env.GITLAB_TOKEN
    }
    response = requests.get(diff_url, headers=headers)

    if response.status_code == 200:
        # Extracting the diff from the response
        changes = response.json()['changes']
        diffs = [change['diff'] for change in changes]
        return '\n'.join(diffs)
    else:
        print("Failed to fetch the diff: ", response.status_code)
        return False
    
def get_mr_reviews():
    # Initialize GitLab client
    gl = gitlab.Gitlab(f'https://{env.GITLAB_DOMAIN}', private_token=env.GITLAB_TOKEN)
    # Get the project

    # Get the project
    project = gl.projects.get(env.REPO_NAME)

    # Get open merge requests
    mrs = project.mergerequests.list(state='opened')

    review_dict_list = []


    for mr in mrs:
        # Check if the MR is opened by the bot
        if mr.author['name'] == 'fumedev[bot]':
            # Get merge request discussions (includes reviews)
            discussions = mr.discussions.list()

            review_dict = {
                    'pull_request_id': mr.id,
                    'pull_request_number': mr.iid,
                    'third_party_id': None,
                    'state':'COMMENTED',
                    'provider':'gitlab',
                    'body': None,
                    'review_comments': []
                }

            for discussion in discussions:
                # Initialize a dictionary for the discussion

                
                for note in discussion.attributes['notes']:
                    # Skip notes from MR author
                    if note['author']['username'] == mr.author['username']:
                        continue

                    if not note['type'] == 'DiffNote':
                        # Set general comment for the discussion
                        review_dict['body'] =  note['body']
                        review_dict['third_party_id'] = discussion.attributes['id']
                    if note['type'] == 'DiffNote':
                        # Append inline comment details
                        review_dict['review_comments'].append({
                            'third_party_id': note['id'],
                            'user': note['author']['name'],
                            'feedback': note['body'],
                            'source_file_path': note['position']['new_path'],
                            'line_number': note['position']['new_line']
                        })
            review_dict['review_comments'] = json.dumps(review_dict['review_comments'])
            review_dict_list.append(review_dict)
    return review_dict_list