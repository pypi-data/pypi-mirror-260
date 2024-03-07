import datetime

import keyring
import requests

SERVICE_NAME = "slamifest"

TOKEN = "token"
REFRESH = "refresh_token"
EXPIRY = "expiry"


def refresh_stored_token(profile: str, refresh_token: str = None):
    if not refresh_token:
        refresh_token = keyring.get_password(SERVICE_NAME, f"{profile}.{REFRESH}")

    tokens = requests.get(
        "https://slack.com/api/tooling.tokens.rotate",
        params={"refresh_token": refresh_token},
    ).json()

    keyring.set_password(SERVICE_NAME, f"{profile}.{TOKEN}", tokens["token"])
    keyring.set_password(SERVICE_NAME, f"{profile}.{REFRESH}", tokens["refresh_token"])
    keyring.set_password(SERVICE_NAME, f"{profile}.{EXPIRY}", str(tokens["exp"]))


def get_token(profile: str):
    exp = int(keyring.get_password(SERVICE_NAME, f"{profile}.{EXPIRY}"))
    now = datetime.datetime.now(datetime.UTC).timestamp()
    if exp <= now:
        refresh_stored_token(profile)

    return keyring.get_password(SERVICE_NAME, f"{profile}.{TOKEN}")
