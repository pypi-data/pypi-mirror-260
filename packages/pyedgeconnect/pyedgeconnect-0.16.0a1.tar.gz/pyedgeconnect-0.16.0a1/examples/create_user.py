import argparse
import getpass
import os

from pyedgeconnect import Orchestrator

# Parse runtime arguments
parser = argparse.ArgumentParser()
parser.add_argument(
    "-o",
    "--orch",
    help="specify Orchestrator URL",
    type=str,
)
args = parser.parse_args()

# Set Orchestrator FQDN/IP via arguments, environment variable,
# or user input
if vars(args)["orch"] is not None:
    orch_url = vars(args)["orch"]
elif os.getenv("ORCH_URL") is not None:
    orch_url = os.getenv("ORCH_URL")
else:
    orch_url = input("Orchstrator IP or FQDN: ")

# Set Orchestrator API Key via environment variable or user input
if os.getenv("ORCH_API_KEY") is not None:
    orch_api_key = os.getenv("ORCH_API_KEY")
else:
    orch_api_key_input = getpass.getpass(
        "Orchstrator API Key (enter to skip): "
    )
    if len(orch_api_key_input) == 0:
        orch_api_key = None
        # Set user and password if present in environment variable
        orch_user = os.getenv("ORCH_USER")
        orch_pw = os.getenv("ORCH_PASSWORD")
    else:
        orch_api_key = orch_api_key_input

# Instantiate Orchestrator with ``log_console`` enabled for
# printing log messages to terminal
orch = Orchestrator(
    orch_url,
    api_key=orch_api_key,
    log_console=True,
    verify_ssl=False,
)

# If not using API key, login to Orchestrator with username/password
if orch_api_key is None:
    # If username/password not in environment variables, prompt user
    if orch_user is None:
        orch_user = input("Enter Orchestrator username: ")
        orch_pw = getpass.getpass("Enter Orchestrator password: ")
    # Check if multi-factor authentication required
    mfa_prompt = input("Are you using MFA for this user (y/n)?: ")
    if mfa_prompt == "y":
        orch.send_mfa(orch_user, orch_pw, temp_code=False)
        token = input("Enter MFA token: ")
    else:
        token = ""
    # Login to Orchestrator
    confirm_auth = orch.login(orch_user, orch_pw, mfacode=token)
    # Check that user/pass authentication works before proceeding
    if confirm_auth:
        pass
    else:
        print("Authentication to Orchestrator Failed")
        exit()
# If API key specified, check that key is valid before proceeding
else:
    confirm_auth = orch.get_orchestrator_hello()
    if confirm_auth != "There was an internal server error.":
        pass
    else:
        print("Authentication to Orchestrator Failed")
        exit()

# set user password details
username = "API_CREATED_USER"
password = 1
confirm_password = 2

# confirm password with interactive user
while password != confirm_password:
    print(
        "\nPassword must be at least 8 characters long and contain "
        + "the following items:\n"
        + "upper case letter, lower case letter, "
        + "a number, a special character\n"
    )
    password = getpass("Enter user's password: ")
    confirm_password = getpass("Confirm user's password: ")
    if password != confirm_password:
        print("Passwords do not match, please try again\n\n")

# create user
# THIS FUNCTION ALSO UPDATES EXISTING USERS
# MAKE SURE NOT TO ACCIDENTLY CHANGE DETAILS
# OF AN EXISTING PRODUCTION USER
orch.create_or_update_user(
    new_user=True,
    user_pk="",
    first_name="first_name",
    last_name="last_name",
    phone="",
    email="jdoe@not-a-real-email.com",
    status="Active",
    role="Network Monitor",
    username=username,
    password=password,
    repeat_password=password,
    two_factor_email=False,
    two_factor_app=False,
)

# retrieve and print user details of newly created user
user_details = orch.get_user(username)
for item in user_details.items():
    print(item)

# if not using API key, logout from Orchestrator
if orch_api_key is None:
    orch.logout()
else:
    pass
