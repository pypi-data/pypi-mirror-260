from urllib import response
import inquirer
import posthog
from supabase import create_client, Client
import json
from fumedev.env import absolute_path
from fumedev.auth.keys import decrypt_message, encrypt_message, load_or_generate_key
from fumedev import env
from supafunc.errors import FunctionsRelayError, FunctionsHttpError


supabase_url = 'https://ftjimequrvncmgwbzcsh.supabase.co'
supabase_public = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ0amltZXF1cnZuY21nd2J6Y3NoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDM3Nzc5NjYsImV4cCI6MjAxOTM1Mzk2Nn0.qOQYWOM9wLrFtQYDVWAf59P3_1zkbmw-FeGrDL_U-kw'

supabase = create_client(supabase_url, supabase_public)



def save_credentials(email, password, key):
    encrypted_email = encrypt_message(email, key)
    encrypted_password = encrypt_message(password, key)
    with open(absolute_path('credentials.json'), 'w') as creds_file:
        json.dump({'email': encrypted_email, 'password': encrypted_password}, creds_file)

def try_auto_login():
    key = load_or_generate_key()

    try:
        with open(absolute_path('credentials.json'), 'r') as creds_file:
            creds = json.load(creds_file)
            email = decrypt_message(creds['email'], key)
            password = decrypt_message(creds['password'], key)
            result = supabase.auth.sign_in_with_password({'email': email, 'password': password})
            if 'error' not in result:
                print("Welcome,", email)
                try:
                    resp = supabase.functions.invoke(
                        "create-lite-lmm-user",
                    invoke_options={
                        "body": {"name": "bar"},
                    },
                    )
                except FunctionsHttpError as exception:
                    err = exception.to_dict()
                    print(f"Function returned an error {err.get('message')}")
                    return False
                except FunctionsRelayError as exception:
                    err = exception.to_dict()
                    print(f"Relay error: {err.get('message')}")
                    return False

                env.OPENAI_API_KEY = json.loads(resp)['key']
            
                env.posthog.identify(result.user.id, {'email': email})
                env.USER_ID = result.user.id
                return True
    except Exception as e:
        return False
    return False


def login():
    key = load_or_generate_key()
    if try_auto_login():
        return

    questions = [
        inquirer.Text('email', message="Please enter your email"),
        inquirer.Password('password', message="Please enter your password"),
    ]

    answers = inquirer.prompt(questions)

    email = answers['email']
    password = answers['password']



    try:
        supabase.auth.sign_in_with_password({'email': email, 'password': password})
        print("\nLogin successful, Welcome!\n")

        resp = supabase.functions.invoke(
            "create-lite-lmm-user",
            invoke_options={
            "body": {"name": "bar"},
            },)
        
        env.OPENAI_API_KEY = json.loads(resp)['key']
        save_credentials(email, password,key)

    except Exception as e:
        print("\nLogin failed please try again.\n")
        login()

def try_login(email, password):
    key = load_or_generate_key()

    try:
        result = supabase.auth.sign_in_with_password({'email': email, 'password': password})
        print("\nLogin successful, Welcome!\n")

        resp = supabase.functions.invoke(
            "create-lite-lmm-user",
            invoke_options={
            "body": {"name": "bar"},
            },)
        
        env.OPENAI_API_KEY = json.loads(resp)['key']
        env.posthog.identify(result.user.id, {'email': email})
        env.USER_ID = result.user.id
        save_credentials(email, password,key)
        return True

        

    except Exception as e:
        print("\nLogin failed please try again.\n")
        return False