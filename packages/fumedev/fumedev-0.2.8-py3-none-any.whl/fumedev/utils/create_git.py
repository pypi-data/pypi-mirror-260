import subprocess

def create_git(destination_path):
            # Initialize and commit using subprocess for better error handling
        try:
            subprocess.run(['git', '-C', str(destination_path), 'init'], check=True,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(['git', '-C', str(destination_path), 'add', '.'], check=True,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(['git', '-C', str(destination_path), 'commit', '-m', 'Initial commit'], check=True,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(f"Error during Git operations: {e}")