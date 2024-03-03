import subprocess
import os

from fumedev.env import absolute_path

def get_changed_files(codebase_path=absolute_path('codebase')):
    # Change the current working directory to the codebase
    original_cwd = os.getcwd()  # Remember the original directory to revert back later
    os.chdir(codebase_path)
    
    try:
        # Get staged files
        staged_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True).splitlines()

        # Get unstaged files
        unstaged_files = subprocess.check_output(['git', 'diff', '--name-only'], text=True).splitlines()
        
        # Get untracked files
        untracked_files = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], text=True).splitlines()
        
        # Combine and remove duplicates
        all_changed_files = list(set(staged_files + unstaged_files + untracked_files))  
    finally:
        # Revert back to the original directory
        os.chdir(original_cwd)
    
    return all_changed_files