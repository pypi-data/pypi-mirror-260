import os

from posthog import Posthog
from fumedev import env
from fumedev.git_ops.createPR import submit_code
from fumedev.git_ops.github_ops.app import GithubApp
from fumedev.git_ops.utils import pull_repo
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

env.FILE_FOLDER = os.path.dirname(os.path.abspath(__file__))
os.makedirs(env.USER_HOME_PATH.joinpath('FumeData'), exist_ok=True) 

from dotenv import load_dotenv
from fumedev.gui.app import FumeApp

load_dotenv()
def main():
    app = FumeApp()
    app.run()

if __name__ == "__main__":
    import sentry_sdk

    sentry_sdk.init(
        dsn="https://e7d25c029a18008af886845658f130b0@o4506832139190272.ingest.sentry.io/4506832142532608",
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
    if env.CLOUD_HOSTED and env.REPO_SERVICE == 'GITHUB':
        env.GITHUB_APP =  GithubApp()
    if env.CLOUD_HOSTED:
        from fumedev.slack_app.app import start_app
        env.posthog.identify(  
            'slack-1', 
        { 'email': 'slack-1@fumedev.com'}
        )
        env.USER_ID = 'slack-1'

        start_app()
    else:
        try:
            main()
        except Exception as e:
            sentry_sdk.capture_exception(e)

